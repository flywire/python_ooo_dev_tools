"""
Module for managing paragraph Drop Caps.

.. versionadded:: 0.9.0
"""
from __future__ import annotations
from typing import Tuple, cast, Type, TypeVar, overload

from .....events.args.cancel_event_args import CancelEventArgs
from .....events.args.key_val_cancel_args import KeyValCancelArgs
from .....exceptions import ex as mEx
from .....meta.static_prop import static_prop
from .....utils import lo as mLo
from .....utils import props as mProps
from ....kind.format_kind import FormatKind
from ....style_base import StyleMulti
from ....writer.style.char.kind import StyleCharKind as StyleCharKind
from ...structs.drop_cap_struct import DropCapStruct

_TDropCaps = TypeVar(name="_TDropCaps", bound="DropCaps")


class DropCapFmt(DropCapStruct):
    """
    Paragraph Drop Cap

    Any properties starting with ``prop_`` set or get current instance values.

    All methods starting with ``fmt_`` can be used to chain together properties.

    .. versionadded:: 0.9.0
    """

    def _supported_services(self) -> Tuple[str, ...]:
        try:
            return self._supported_services_values
        except AttributeError:
            self._supported_services_values = (
                "com.sun.star.style.ParagraphProperties",
                "com.sun.star.text.TextContent",
                "com.sun.star.style.ParagraphStyle",
            )
        return self._supported_services_values

    def _get_property_name(self) -> str:
        try:
            return self._property_name
        except AttributeError:
            self._property_name = "DropCapFormat"
        return self._property_name

    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        try:
            return self._fromat_kind_prop
        except AttributeError:
            self._fromat_kind_prop = FormatKind.PARA | FormatKind.TXT_CONTENT
        return self._fromat_kind_prop


class DropCaps(StyleMulti):
    """
    Paragraph Drop Caps

    .. versionadded:: 0.9.0
    """

    # region init

    def __init__(
        self,
        *,
        count: int = 0,
        spaces: float = 0.0,
        lines: int = 3,
        style: StyleCharKind | str | None = None,
        whole_word: bool | None = None,
    ) -> None:
        """
        Constructor

        Args:
            count (int): Specifies the number of characters in the drop cap. Must be from ``0`` to ``255``.
            spaces (float): Specifies the distance between the drop cap in the following text (in mm units)
            lines (int): Specifies the number of lines used for a drop cap. Must be from ``0`` to ``255``.
            style (StyleCharKind, str, optional): Specifies the character style name for drop caps.
            whole_word (bool, optional): specifies if Drop Cap is applied to the whole first word.
        Returns:
            None:

        Note:
            If ``count==-1`` then only ``style`` can be updated.
            If ``count==0`` then all other argumnets are ignored and instance set to remove drop caps when ``apply()`` is called.

        Warning:
            This class may uses dispatch commands and may not suitable for use in headless mode.

            Due to LibreOffice bug this class will use a dispatch command if ``style`` is set to empty string.
        """
        # https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1ParagraphProperties-members.html

        # if count == -1 then do not include DropCapFmt. only update style
        # if count = 0 then default to no drop cap values
        dc = None
        init_vars = {}

        if count == -1:
            if not style is None:
                init_vars["DropCapCharStyleName"] = str(style)
        elif count == 0:
            # set defatults to apply no drop caps
            whole_word = False
            style = ""
            init_vars["DropCapWholeWord"] = False
            init_vars["DropCapCharStyleName"] = ""
            dc = DropCapFmt(count=0, distance=0, lines=0)
        elif count > 0:
            dc = DropCapFmt(count=count, distance=round(spaces * 100), lines=lines)
            if not whole_word is None:
                init_vars["DropCapWholeWord"] = whole_word
                if whole_word:
                    # when whole word is set the count must be 1 (for one word)
                    dc.prop_count = 1
            if not style is None:
                init_vars["DropCapCharStyleName"] = str(style)
        else:
            raise ValueError("Count must not be less then -1")

        super().__init__(**init_vars)
        if dc:
            self._set_style_dc(dc)

    # endregion init

    # region methods

    def dispatch_reset(self) -> None:
        """
        Resets the cursor at is current position/selection to remove any Drop Caps Formatting using a dispatch command.

        Returns:
            None:

        Example:

            .. code-block:: python

                dc = DropCaps(count=1, style=StyleCharKind.DROP_CAPS)
                Write.append_para(cursor=cursor, text="Hello World!", styles=(dc,))
                dc.dispatch_reset()
        """
        drop_cap_args = {
            "FormatDropcap.Lines": 1,
            "FormatDropcap.Count": 1,
            "FormatDropcap.Distance": 0,
            "FormatDropcap.WholeWord": False,
        }
        drop_cap_props = mProps.Props.make_props(**drop_cap_args)
        mLo.Lo.dispatch_cmd("FormatDropcap", drop_cap_props)
        # mLo.Lo.delay(300)
        mLo.Lo.dispatch_cmd("SetDropCapCharStyleName", mProps.Props.make_props(CharStyleName=""))
        # mLo.Lo.delay(300)

    def on_property_setting(self, event_args: KeyValCancelArgs) -> None:
        """
        Triggers for each property that is set

        Args:
            event_args (KeyValueCancelArgs): Event Args
        """
        if event_args.key == "DropCapCharStyleName":
            # DropCapCharStyleName will not allow itself to be set if it has empty string
            # as a value, even though it ia a string and will take a string value of any valid
            # character style.
            if event_args.value is None or event_args.value == "":
                # instruct Props.set to call set_default()
                event_args.default = True
            super().on_property_setting(event_args)

    def _set_style_dc(self, dc: DropCapFmt | None) -> None:
        if dc is None:
            self._remove_style("drop_cap")
            return
        dc._prop_parent = self
        self._set_style("drop_cap", dc, *dc.get_attrs())

    def _on_modifing(self, event: CancelEventArgs) -> None:
        if self._is_default_inst:
            raise ValueError("Modifying a default instance is not allowed")
        return super()._on_modifing(event)

    def _supported_services(self) -> Tuple[str, ...]:
        try:
            return self._supported_services_values
        except AttributeError:
            self._supported_services_values = (
                "com.sun.star.style.ParagraphProperties",
                "com.sun.star.text.TextContent",
                "com.sun.star.style.ParagraphStyle",
            )
        return self._supported_services_values

    # region from_obj()
    @overload
    @classmethod
    def from_obj(cls: Type[_TDropCaps], obj: object) -> _TDropCaps:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_TDropCaps], obj: object, **kwargs) -> _TDropCaps:
        ...

    @classmethod
    def from_obj(cls: Type[_TDropCaps], obj: object, **kwargs) -> _TDropCaps:
        """
        Gets instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            DropCaps: ``DropCaps`` instance that represents ``obj`` Drop Caps.
        """
        inst = cls(**kwargs)
        if not inst._is_valid_obj(obj):
            raise mEx.NotSupportedError(f'Object is not supported for conversion to "{cls.__name__}"')
        dc = DropCapFmt.from_obj(obj)
        inst._set_style_dc(dc)

        whole_word = cast(bool, mProps.Props.get(obj, "DropCapWholeWord"))
        style = cast(str, mProps.Props.get(obj, "DropCapCharStyleName"))
        if not whole_word is None:
            inst._set("DropCapWholeWord", whole_word)
        if not style is None:
            inst._set("DropCapCharStyleName", style)
        return inst

    # endregion from_obj()
    # endregion methods

    # region properties

    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        try:
            return self._fromat_kind_prop
        except AttributeError:
            self._fromat_kind_prop = FormatKind.PARA | FormatKind.TXT_CONTENT
        return self._fromat_kind_prop

    @property
    def prop_inner(self) -> DropCapFmt | None:
        """Gets Drop Caps Format instance"""
        try:
            return self._direct_inner
        except AttributeError:
            self._direct_inner = cast(DropCapFmt, self._get_style_inst("drop_cap"))
        return self._direct_inner

    @static_prop
    def default() -> DropCaps:  # type: ignore[misc]
        """Gets ``DropCaps`` default. Static Property."""
        try:
            return DropCaps._DEFAULT_INST
        except AttributeError:
            inst = DropCaps(count=0)
            inst._is_default_inst = True
            DropCaps._DEFAULT_INST = inst
        return DropCaps._DEFAULT_INST

    # endregion properties