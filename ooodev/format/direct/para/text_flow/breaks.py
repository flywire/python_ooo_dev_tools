"""
Modele for managing paragraph breaks.

.. versionadded:: 0.9.0
"""
from __future__ import annotations
from typing import Tuple, overload, cast, Type, TypeVar

from .....events.args.cancel_event_args import CancelEventArgs
from .....exceptions import ex as mEx
from .....meta.static_prop import static_prop
from .....utils import lo as mLo
from .....utils import props as mProps
from ....kind.format_kind import FormatKind
from ....style_base import StyleBase

from ooo.dyn.style.break_type import BreakType as BreakType

_TBreaks = TypeVar(name="_TBreaks", bound="Breaks")


class Breaks(StyleBase):
    """
    Paragraph Breaks

    Any properties starting with ``prop_`` set or get current instance values.

    .. versionadded:: 0.9.0
    """

    # region init

    def __init__(self, *, type: BreakType | None = None, style: str | None = None, num: int | None = None) -> None:
        """
        Constructor

        Args:
            type (BreakType, optional): Break type.
            style (str, optional): Style to apply to break.
            num (int, optional): Page number to apply to break.

        Returns:
            None:

        Note:
            If argument ``type`` is ``None`` then all other argument are ignored
        """
        # https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1ParagraphProperties-members.html
        # Defatul for writer is BreakType.NONE
        # BreakType controls the dialog insert checkbox

        # pg_style only applies
        # Dialog position is set by the type: e.g. BreakType.PAGE_AFTER Type is Page and Position is After
        # When BreakType.PAGE_AFTER or COLUMN_AFTER page style is not used.

        if type is None:
            # everything depends on a BreakType
            super().__init__()
            return

        init_vals = {"BreakType": type}
        if type in (BreakType.PAGE_BEFORE, BreakType.COLUMN_BEFORE, BreakType.COLUMN_BOTH, BreakType.PAGE_BOTH):

            if not style is None:
                # # pg_style is only valid when BreakType.COLUMN_BEFORE or BreakType.PAGE_BEFORE

                # LibreOffice Dev Tools report this property as readonly.
                # api does not.
                # PageStyleName: contains the name of the current page style.

                # init_vals["PageStyleName"] = pg_style

                # PageDescName: If this property is set, it creates a page break before the paragraph
                # it belongs to and assigns the value as the name of the new page style sheet to use.
                init_vals["PageDescName"] = style

        if "PageDescName" in init_vals and not num is None:
            # pg_num is only valid when BreakType.COLUMN_BEFORE or BreakType.PAGE_BEFORE AND
            # page style is set (pg_style)
            init_vals["PageNumberOffset"] = num

        super().__init__(**init_vals)

    # endregion init

    # region methods

    def _supported_services(self) -> Tuple[str, ...]:
        try:
            return self._supported_services_values
        except AttributeError:
            self._supported_services_values = (
                "com.sun.star.style.ParagraphProperties",
                "com.sun.star.style.ParagraphStyle",
            )
        return self._supported_services_values

    def _on_modifing(self, event: CancelEventArgs) -> None:
        if self._is_default_inst:
            raise ValueError("Modifying a default instance is not allowed")
        return super()._on_modifing(event)

    # region apply()
    @overload
    def apply(self, obj: object) -> None:
        ...

    def apply(self, obj: object, **kwargs) -> None:
        """
        Applies break properties to ``obj``

        Args:
            obj (object): UNO object that supports ``com.sun.star.style.ParagraphProperties`` service.

        Returns:
            None:
        """
        try:
            super().apply(obj, **kwargs)
        except mEx.MultiError as e:
            mLo.Lo.print(f"{self.__class__.__name__}.apply(): Unable to set Property")
            for err in e.errors:
                mLo.Lo.print(f"  {err}")

    # endregion apply()

    # region from_obj()
    @overload
    @classmethod
    def from_obj(cls: Type[_TBreaks], obj: object) -> _TBreaks:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_TBreaks], obj: object, **kwargs) -> _TBreaks:
        ...

    @classmethod
    def from_obj(cls: Type[_TBreaks], obj: object, **kwargs) -> _TBreaks:
        """
        Gets instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            Breaks: ``Breaks`` instance that represents ``obj`` break properties.
        """
        nu = cls(**kwargs)
        if not nu._is_valid_obj(obj):
            raise mEx.NotSupportedError(f'Object is not supported for conversion to "{cls.__name__}"')

        t = mProps.Props.get(obj, "BreakType", None)
        style = mProps.Props.get(obj, "PageDescName", None)
        num = mProps.Props.get(obj, "PageNumberOffset", None)
        return cls(type=t, style=style, num=num, **kwargs)

    # endregion from_obj()

    # endregion methods

    # region properties
    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        try:
            return self._format_kind_prop
        except AttributeError:
            self._format_kind_prop = FormatKind.PARA
        return self._format_kind_prop

    @property
    def prop_type(self) -> BreakType | None:
        """Gets break type"""
        return self._get("BreakType")

    @property
    def prop_style(self) -> str | None:
        """Gets Break Style"""
        return self._get("PageDescName")

    @property
    def prop_num(self) -> int | None:
        """Gets Page number to apply to break"""
        return self._get("PageNumberOffset")

    @static_prop
    def default() -> Breaks:  # type: ignore[misc]
        """Gets ``Breaks`` default. Static Property."""
        try:
            return Breaks._DEFAULT_INST
        except AttributeError:
            Breaks._DEFAULT_INST = Breaks(type=BreakType.NONE)
            Breaks._DEFAULT_INST._is_default_inst = True
        return Breaks._DEFAULT_INST

    # endregion properties