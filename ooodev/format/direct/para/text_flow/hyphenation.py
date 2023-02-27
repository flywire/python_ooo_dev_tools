"""
Modele for managing paragraph hyphenation.

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

_THyphenation = TypeVar(name="_THyphenation", bound="Hyphenation")


class Hyphenation(StyleBase):
    """
    Paragraph Hypehation

    Any properties starting with ``prop_`` set or get current instance values.

    All methods starting with ``fmt_`` can be used to chain together properties.

    .. versionadded:: 0.9.0
    """

    # region init

    def __init__(
        self,
        *,
        auto: bool | None = None,
        no_caps: bool | None = None,
        start_chars: int | None = None,
        end_chars: int | None = None,
        max: int | None = None,
    ) -> None:
        """
        Constructor

        Args:
            auto (bool, optional): Hyphenate automatically.
            no_caps (bool, optional): Don't hyphenate word in caps.
            start_chars (int, optional): Characters at line begin.
            end_chars (int, optional): charactors at line end.
            max (int, optional): Maximum consecutive hyphenated lines.

        Returns:
            None:

        Note:
            If argument ``auto`` is ``False`` then all other argument have no effect.
        """
        # https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1ParagraphProperties-members.html
        init_vals = {}
        if not auto is None:
            init_vals["ParaIsHyphenation"] = auto

        if not start_chars is None:
            init_vals["ParaHyphenationMaxLeadingChars"] = start_chars

        if not end_chars is None:
            init_vals["ParaHyphenationMaxTrailingChars"] = end_chars

        if not no_caps is None:
            init_vals["ParaHyphenationNoCaps"] = no_caps

        if not max is None:
            init_vals["ParaHyphenationMaxHyphens"] = max

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
        Applies hypenation properties to ``obj``

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
    def from_obj(cls: Type[_THyphenation], obj: object) -> _THyphenation:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_THyphenation], obj: object, **kwargs) -> _THyphenation:
        ...

    @classmethod
    def from_obj(cls: Type[_THyphenation], obj: object, **kwargs) -> _THyphenation:
        """
        Gets instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            Hyphenation: ``Hyphenation`` instance that represents ``obj`` hypenation properties.
        """
        inst = cls(**kwargs)
        if not inst._is_valid_obj(obj):
            raise mEx.NotSupportedError(f'Object is not supported for conversion to "{cls.__name__}"')

        def set_prop(key: str, indent: Hyphenation):
            nonlocal obj
            val = mProps.Props.get(obj, key, None)
            if not val is None:
                indent._set(key, val)

        set_prop("ParaIsHyphenation", inst)
        set_prop("ParaHyphenationMaxLeadingChars", inst)
        set_prop("ParaHyphenationMaxTrailingChars", inst)
        set_prop("ParaHyphenationNoCaps", inst)
        set_prop("ParaHyphenationMaxHyphens", inst)

        return inst

    # endregion from_obj()

    # endregion methods

    # region style methods
    def fmt_auto(self: _THyphenation, value: bool | None) -> _THyphenation:
        """
        Gets copy of instance with auto set or removed

        Args:
            value (bool | None): auto value

        Returns:
            Hyphenation: ``Hyphenation`` instance
        """
        cp = self.copy()
        cp.prop_auto = value
        return cp

    def fmt_no_caps(self: _THyphenation, value: bool | None) -> _THyphenation:
        """
        Gets copy of instance with no caps set or removed

        Args:
            value (bool | None): no caps value

        Returns:
            Hyphenation: ``Hyphenation`` instance
        """
        cp = self.copy()
        cp.prop_no_caps = value
        return cp

    def fmt_start_chars(self: _THyphenation, value: int | None) -> _THyphenation:
        """
        Gets copy of instance with start chars set or removed

        Args:
            value (bool | None): start chars value

        Returns:
            Hyphenation: ``Hyphenation`` instance
        """
        cp = self.copy()
        cp.prop_start_chars = value
        return cp

    def fmt_end_chars(self: _THyphenation, value: int | None) -> _THyphenation:
        """
        Gets copy of instance with end chars set or removed

        Args:
            value (bool | None): end chars value

        Returns:
            Hyphenation: ``Hyphenation`` instance
        """
        cp = self.copy()
        cp.prop_end_chars = value
        return cp

    def fmt_max_chars(self: _THyphenation, value: int | None) -> _THyphenation:
        """
        Gets copy of instance with max set or removed

        Args:
            value (bool | None): max value

        Returns:
            Hyphenation: ``Hyphenation`` instance
        """
        cp = self.copy()
        cp.prop_max = value
        return cp

    # endregion style methods

    # region Style Properties
    @property
    def auto(self: _THyphenation) -> _THyphenation:
        """
        Gets instance with Hyphenate automatically set to ``True``.
        """
        cp = self.copy()
        cp.prop_auto = True
        return cp

    @property
    def no_caps(self: _THyphenation) -> _THyphenation:
        """
        Gets instance with no caps set to ``True``.
        """
        cp = self.copy()
        cp.prop_no_caps = True
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
    def prop_auto(self) -> bool | None:
        """Gets/Sets Hyphenate automatically."""
        return self._get("ParaIsHyphenation")

    @prop_auto.setter
    def prop_auto(self, value: bool | None):
        if value is None:
            self._remove("ParaIsHyphenation")
            return
        self._set("ParaIsHyphenation", value)

    @property
    def prop_no_caps(self) -> bool | None:
        """Gets/Sets if hyphenate word in caps."""
        return self._get("ParaHyphenationNoCaps")

    @prop_no_caps.setter
    def prop_no_caps(self, value: bool | None):
        if value is None:
            self._remove("ParaHyphenationNoCaps")
            return
        self._set("ParaHyphenationNoCaps", value)

    @property
    def prop_start_chars(self) -> int | None:
        """Gets/Sets number of characters at line begin."""
        return self._get("ParaHyphenationMaxLeadingChars")

    @prop_start_chars.setter
    def prop_start_chars(self, value: int | None):
        if value is None:
            self._remove("ParaHyphenationMaxLeadingChars")
            return
        self._set("ParaHyphenationMaxLeadingChars", value)

    @property
    def prop_end_chars(self) -> int | None:
        """Gets/Sets number of characters at line end."""
        return self._get("ParaHyphenationMaxTrailingChars")

    @prop_end_chars.setter
    def prop_end_chars(self, value: int | None):
        if value is None:
            self._remove("ParaHyphenationMaxTrailingChars")
            return
        self._set("ParaHyphenationMaxTrailingChars", value)

    @property
    def prop_max(self) -> int | None:
        """Gets/Sets maximum consecutive hyphenated lines."""
        return self._get("ParaHyphenationMaxHyphens")

    @prop_max.setter
    def prop_max(self, value: int | None):
        if value is None:
            self._remove("ParaHyphenationMaxHyphens")
            return
        self._set("ParaHyphenationMaxHyphens", value)

    @static_prop
    def default() -> Hyphenation:  # type: ignore[misc]
        """Gets ``Hyphenation`` default. Static Property."""
        try:
            return Hyphenation._DEFAULT_INST
        except AttributeError:
            Hyphenation._DEFAULT_INST = Hyphenation(auto=False, no_caps=False, start_chars=2, end_chars=2, max=0)
            Hyphenation._DEFAULT_INST._is_default_inst = True
        return Hyphenation._DEFAULT_INST

    # endregion properties