"""
Module for Shadow format (``LineSpacing``) struct.

.. versionadded:: 0.9.0
"""
# region imports
from __future__ import annotations
from typing import Dict, Tuple, Type, TypeVar, cast, overload, TYPE_CHECKING
from enum import Enum
from numbers import Real

import uno
from ....events.event_singleton import _Events
from ....meta.static_prop import static_prop
from ....utils import props as mProps
from ...kind.format_kind import FormatKind
from ...style_base import StyleBase, EventArgs, CancelEventArgs, FormatNamedEvent
from ....utils.unit_convert import UnitConvert, Length
from ....utils.type_var import T

from ooo.dyn.style.line_spacing import LineSpacing as UnoLineSpacing

_TLineSpacingStruct = TypeVar(name="_TLineSpacingStruct", bound="LineSpacingStruct")


class ModeKind(Enum):
    """Mode Kind for line spacing"""

    # Enum value, mode, default
    SINGLE = (0, 0, 100)  # zero value,
    """Single Line Spacing ``1mm``"""
    LINE_1_15 = (1, 0, 115)  # zero value, value
    """Line Spacing ``1.15mm``"""
    LINE_1_5 = (2, 0, 150)
    """Line Spacing ``1.5mm``"""
    DOUBLE = (3, 0, 200)
    """Double line spacing ``2mm``"""
    PROPORTIONAL = (4, 0, 0)  # PERCENTAGE, No conversion onf height value 98 % = 98 MM100
    """Proportional line spacing"""
    AT_LEAST = (5, 1, 0)  # IN 1/100 MM
    """At least line spacing"""
    LEADING = (6, 2, 0)  # in 1/100 MM
    """Leading Line Spacing"""
    FIXED = (7, 3, 0)  # in 1/100 MM
    """Fixed Line Spacing"""

    def __int__(self) -> int:
        return self.value[2]

    def get_mode(self) -> int:
        return self.value[1]

    def get_enum_val(self) -> int:
        return self.value[0]

    @staticmethod
    def from_uno(ls: UnoLineSpacing) -> ModeKind:
        """Converts UNO ``LineSpacing`` struct to ``ModeKind`` enum."""
        mode = ls.Mode
        val = ls.Height
        if mode == 0:
            if val == 100:
                return ModeKind.SINGLE
            if val == 115:
                return ModeKind.LINE_1_15
            if val == 150:
                return ModeKind.LINE_1_5
            if val == 200:
                return ModeKind.DOUBLE
            else:
                return ModeKind.PROPORTIONAL
        if mode == 1:
            return ModeKind.AT_LEAST
        if mode == 2:
            return ModeKind.LEADING
        if mode == 3:
            return ModeKind.FIXED
        raise ValueError("Uanble to convert uno LineSpacing object to ModeKind Enum")


# endregion imports
class LineSpacingStruct(StyleBase):
    """
    Line Spacing struct
    """

    # region init

    def __init__(self, mode: ModeKind = ModeKind.SINGLE, value: Real = 0) -> None:
        """
        Constructor

        Args:
            mode (LineMode, optional): This value specifies the way the spacing is specified.
            value (Real, optional): This value specifies the spacing in regard to Mode.

        Raises:
            ValueError: If ``value`` are less than zero.

        Note:
            If ``LineMode`` is ``SINGLE``, ``LINE_1_15``, ``LINE_1_5``, or ``DOUBLE`` then ``value`` is ignored.

            If ``LineMode`` is ``AT_LEAST``, ``LEADING``, or ``FIXED`` then ``value`` is a float (``in mm uints``).

            If ``LineMode`` is ``PROPORTIONAL`` then value is an int representing percentage.
            For example ``95`` equals ``95%``, ``130`` equals ``130%``
        """
        if value < 0:
            raise ValueError("mode must be a positive number")

        self._line_mode = mode
        self._mode = mode.get_mode()
        self._value = int(mode)
        enum_val = mode.get_enum_val()

        if mode == ModeKind.PROPORTIONAL:
            # no conversion
            self._value = value

        elif enum_val >= 5:
            self._value = UnitConvert.convert(num=value, frm=Length.MM, to=Length.MM100)

        super().__init__()

    # endregion init

    # region methods
    def __eq__(self, other: object) -> bool:
        ls2: UnoLineSpacing = None
        if isinstance(other, LineSpacingStruct):
            ls2 = other.get_uno_struct()
        elif getattr(other, "typeName", None) == "com.sun.star.style.LineSpacing":
            ls2 = other
        if ls2:
            ls1 = self.get_uno_struct()
            return ls1.Height == ls2.Height and ls1.Mode == ls2.Mode
        return False

    def _supported_services(self) -> Tuple[str, ...]:
        try:
            return self._supported_services_values
        except AttributeError:
            self._supported_services_values = ()
        return self._supported_services_values

    def _on_modifing(self, event: CancelEventArgs) -> None:
        if self._is_default_inst:
            raise ValueError("Modifying a default instance is not allowed")
        return super()._on_modifing(event)

    def _get_property_name(self) -> str:
        try:
            return self._property_name
        except AttributeError:
            self._property_name = "ParaLineSpacing"
        return self._property_name

    def get_attrs(self) -> Tuple[str, ...]:
        """
        Gets the attributes that are slated for change in the current instance

        Returns:
            Tuple(str, ...): Tuple of attribures
        """
        return (self._get_property_name(),)

    # region copy()
    @overload
    def copy(self: _TLineSpacingStruct) -> _TLineSpacingStruct:
        ...

    @overload
    def copy(self: _TLineSpacingStruct, **kwargs) -> _TLineSpacingStruct:
        ...

    def copy(self: _TLineSpacingStruct, **kwargs) -> _TLineSpacingStruct:
        nu = self.__class__(mode=self._mode, height=self._value, **kwargs)
        dv = self._get_properties()
        if dv:
            nu._update(dv)
        return nu

    # endregion copy()

    # region apply()

    @overload
    def apply(self, obj: object, *, keys: Dict[str, str]) -> None:
        ...

    @overload
    def apply(self, obj: object) -> None:
        ...

    def apply(self, obj: object, **kwargs) -> None:
        """
        Applies style to object

        Args:
            obj (object): Object that contains a ``LineSpacing`` property.
            keys: (Dict[str, str], optional): key map for properties.
                Can be ``spacing`` which maps to ``ParaLineSpacing`` by default.

        :events:
            .. cssclass:: lo_event

                - :py:attr:`~.events.format_named_event.FormatNamedEvent.STYLE_APPLYING` :eventref:`src-docs-event-cancel`
                - :py:attr:`~.events.format_named_event.FormatNamedEvent.STYLE_APPLYED` :eventref:`src-docs-event`


        Returns:
            None:
        """
        if not self._is_valid_obj(obj):
            # will not apply on this class but may apply on child classes
            self._print_not_valid_obj("apply()")
            return
        cargs = CancelEventArgs(source=f"{self.apply.__qualname__}")
        cargs.event_data = self
        self.on_applying(cargs)
        if cargs.cancel:
            return
        _Events().trigger(FormatNamedEvent.STYLE_APPLYING, cargs)
        if cargs.cancel:
            return

        keys = {"spacing": self._get_property_name()}
        if "keys" in kwargs:
            keys.update(kwargs["keys"])
        key = keys["spacing"]
        mProps.Props.set(obj, **{key: self.get_uno_struct()})
        eargs = EventArgs.from_args(cargs)
        self.on_applied(eargs)
        _Events().trigger(FormatNamedEvent.STYLE_APPLIED, eargs)

    # endregion apply()

    def get_uno_struct(self) -> UnoLineSpacing:
        """
        Gets UNO ``Gradient`` from instance.

        Returns:
            Gradient: ``Gradient`` instance
        """
        return UnoLineSpacing(Mode=self._mode, Height=self._value)

    # region from_line_spacing()
    @overload
    @classmethod
    def from_line_spacing(cls: Type[_TLineSpacingStruct], ln_spacing: UnoLineSpacing) -> _TLineSpacingStruct:
        ...

    @overload
    @classmethod
    def from_line_spacing(cls: Type[_TLineSpacingStruct], ln_spacing: UnoLineSpacing, **kwargs) -> _TLineSpacingStruct:
        ...

    @classmethod
    def from_line_spacing(cls: Type[_TLineSpacingStruct], ln_spacing: UnoLineSpacing, **kwargs) -> _TLineSpacingStruct:
        """
        Converts a UNO ``LineSpacing`` struct into a ``LineSpacingStruct``

        Args:
            ln_spacing (UnoLineSpacing): UNO ``LineSpacing`` object.

        Returns:
            LineSpacingStruct: ``LineSpacingStruct`` set with Line spacing properties.
        """
        inst = cls(**kwargs)
        inst._mode = ln_spacing.Mode
        inst._value = ln_spacing.Height
        inst._line_mode = ModeKind.from_uno(ln_spacing)
        return inst

    # endregion from_line_spacing()

    # endregion methods

    # region Properties
    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        try:
            return self._format_kind_prop
        except AttributeError:
            self._format_kind_prop = FormatKind.STRUCT
        return self._format_kind_prop

    @property
    def prop_mode(self) -> ModeKind:
        """Gets mode value"""
        return self._line_mode

    @property
    def prop_value(self) -> Real:
        """Gets the spacing value in regard to Mode"""
        return self._value

    @static_prop
    def default() -> LineSpacingStruct:  # type: ignore[misc]
        """Gets empty Line Spacing. Static Property."""
        try:
            return LineSpacingStruct._DEFAULT_INST
        except AttributeError:
            LineSpacingStruct._DEFAULT_INST = LineSpacingStruct(ModeKind.SINGLE, 0)
            LineSpacingStruct._DEFAULT_INST._is_default_inst = True
        return LineSpacingStruct._DEFAULT_INST

    # endregion Properties