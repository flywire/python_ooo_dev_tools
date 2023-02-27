"""
Modele for managing paragraph padding.

.. versionadded:: 0.9.0
"""
from __future__ import annotations
from typing import Tuple, cast, overload, Type, TypeVar

from .....events.args.cancel_event_args import CancelEventArgs
from .....exceptions import ex as mEx
from .....meta.static_prop import static_prop
from .....utils import lo as mLo
from .....utils import props as mProps
from ....kind.format_kind import FormatKind
from ....style_base import StyleBase

_TIndent = TypeVar(name="_TIndent", bound="Indent")


class Indent(StyleBase):
    """
    Paragraph Indent

    Any properties starting with ``prop_`` set or get current instance values.

    All methods starting with ``fmt_`` can be used to chain together properties.

    .. versionadded:: 0.9.0
    """

    # region init

    def __init__(
        self,
        *,
        before: float | None = None,
        after: float | None = None,
        first: float | None = None,
        auto: bool | None = None,
    ) -> None:
        """
        Constructor

        Args:
            before (float, optional): Determines the left margin of the paragraph (in ``mm`` units).
            after (float, optional): Determines the right margin of the paragraph (in ``mm`` units).
            first (float, optional): specifies the indent for the first line (in ``mm`` units).
            auto (bool, optional): Determines if the first line should be indented automatically.
        Returns:
            None:
        """
        # https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1ParagraphProperties-members.html
        init_vals = {}

        if not before is None:
            init_vals["ParaLeftMargin"] = round(before * 100)

        if not after is None:
            init_vals["ParaRightMargin"] = round(after * 100)

        if not first is None:
            init_vals["ParaFirstLineIndent"] = round(first * 100)

        if not auto is None:
            init_vals["ParaIsAutoFirstLineIndent"] = auto
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
        Applies writing mode to ``obj``

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
    def from_obj(cls: Type[_TIndent], obj: object) -> _TIndent:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_TIndent], obj: object, **kwargs) -> _TIndent:
        ...

    @classmethod
    def from_obj(cls: Type[_TIndent], obj: object, **kwargs) -> _TIndent:
        """
        Gets instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            Indent: ``Indent`` instance that represents ``obj`` writing mode.
        """
        inst = cls(**kwargs)
        if not inst._is_valid_obj(obj):
            raise mEx.NotSupportedError(f'Object is not supported for conversion to "{cls.__name__}"')

        def set_prop(key: str, indent: Indent):
            nonlocal obj
            val = mProps.Props.get(obj, key, None)
            if not val is None:
                indent._set(key, val)

        set_prop("ParaLeftMargin", inst)
        set_prop("ParaRightMargin", inst)
        set_prop("ParaFirstLineIndent", inst)
        set_prop("ParaIsAutoFirstLineIndent", inst)
        return inst

    # endregion from_obj()

    # endregion methods

    # region style methods
    def fmt_before(self: _TIndent, value: float | None) -> _TIndent:
        """
        Gets a copy of instance with before margin set or removed

        Args:
            value (float | None): Margin value (in mm units).

        Returns:
            Indent: Indent instance
        """
        cp = self.copy()
        cp.prop_before = value
        return cp

    def fmt_after(self: _TIndent, value: float | None) -> _TIndent:
        """
        Gets a copy of instance with after margin set or removed

        Args:
            value (float | None): Margin value (in mm units).

        Returns:
            Indent: Indent instance
        """
        cp = self.copy()
        cp.prop_after = value
        return cp

    def fmt_first(self: _TIndent, value: float | None) -> _TIndent:
        """
        Gets a copy of instance with first indent margin set or removed

        Args:
            value (float | None): Margin value (in mm units).

        Returns:
            Indent: Indent instance
        """
        cp = self.copy()
        cp.prop_after = value
        return cp

    def fmt_auto(self: _TIndent, value: bool | None) -> _TIndent:
        """
        Gets a copy of instance with auto set or removed

        Args:
            value (bool | None): Auto value.

        Returns:
            Indent: Indent instance
        """
        cp = self.copy()
        cp.prop_auto = value
        return cp

    # endregion style methods

    # region Style Properties
    @property
    def auto(self: _TIndent) -> _TIndent:
        """Gets copy of instance with auto set"""
        cp = self.copy()
        cp.prop_auto = True
        return cp

    # endregion Style Properties

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
    def prop_before(self) -> float | None:
        """Gets/Sets the left margin of the paragraph (in mm units)."""
        pv = cast(int, self._get("ParaLeftMargin"))
        if pv is None:
            return None
        if pv == 0:
            return 0.0
        return float(pv / 100)

    @prop_before.setter
    def prop_before(self, value: float | None):
        if value is None:
            self._remove("ParaLeftMargin")
            return
        self._set("ParaLeftMargin", value)

    @property
    def prop_after(self) -> float | None:
        """Gets/Sets the right margin of the paragraph (in mm units)."""
        pv = cast(int, self._get("ParaRightMargin"))
        if pv is None:
            return None
        if pv == 0:
            return 0.0
        return float(pv / 100)

    @prop_after.setter
    def prop_after(self, value: float | None):
        if value is None:
            self._remove("ParaRightMargin")
            return
        self._set("ParaRightMargin", value)

    @property
    def prop_first(self) -> float | None:
        """Gets/Sets the indent for the first line (in mm units)."""
        pv = cast(int, self._get("ParaFirstLineIndent"))
        if pv is None:
            return None
        if pv == 0:
            return 0.0
        return float(pv / 100)

    @prop_first.setter
    def prop_first(self, value: float | None):
        if value is None:
            self._remove("ParaFirstLineIndent")
            return
        self._set("ParaFirstLineIndent", value)

    @property
    def prop_auto(self) -> bool | None:
        """Gets/Sets if the first line should be indented automatically"""
        return self._get("ParaIsAutoFirstLineIndent")

    @prop_auto.setter
    def prop_auto(self, value: bool | None):
        if value is None:
            self._remove("ParaIsAutoFirstLineIndent")
            return
        self._set("ParaIsAutoFirstLineIndent", value)

    @static_prop
    def default() -> Indent:  # type: ignore[misc]
        """Gets ``Indent`` default. Static Property."""
        try:
            return Indent._DEFAULT_INST
        except AttributeError:
            Indent._DEFAULT_INST = Indent(before=0.0, after=0.0, first=0.0, auto=False)
            Indent._DEFAULT_INST._is_default_inst = True
        return Indent._DEFAULT_INST

    # endregion properties