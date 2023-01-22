"""
Module for Shadow format (``ShadowFormat``) struct.

.. versionadded:: 0.9.0
"""
# region imports
from __future__ import annotations
from typing import Dict, Tuple, cast, overload

from ....events.event_singleton import _Events
from ....meta.static_prop import static_prop
from ....utils import props as mProps
from ....utils.color import Color
from ....utils.color import CommonColor
from ...kind.format_kind import FormatKind
from ...style_base import StyleBase, EventArgs, CancelEventArgs, FormatNamedEvent

import uno
from ooo.dyn.table.shadow_format import ShadowFormat as ShadowFormat
from ooo.dyn.table.shadow_location import ShadowLocation as ShadowLocation


# endregion imports
class Shadow(StyleBase):
    """
    Shadow struct

    Any properties starting with ``prop_`` set or get current instance values.

    All methods starting with ``fmt_`` can be used to chain together properties.

    .. versionadded:: 0.9.0
    """

    # region init
    _EMPTY = None

    def __init__(
        self,
        location: ShadowLocation = ShadowLocation.BOTTOM_RIGHT,
        color: Color = CommonColor.GRAY,
        transparent: bool = False,
        width: float = 1.76,
    ) -> None:
        """
        Constructor

        Args:
            location (ShadowLocation, optional): contains the location of the shadow. Default to ``ShadowLocation.BOTTOM_RIGHT``.
            color (Color, optional):contains the color value of the shadow. Defaults to ``CommonColor.GRAY``.
            transparent (bool, optional): Shadow transparency. Defaults to False.
            width (float, optional): contains the size of the shadow (in mm units). Defaults to ``1.76``.

        Raises:
            ValueError: If ``color`` or ``width`` are less than zero.
        """
        if color < 0:
            raise ValueError("color must be a positive number")
        if width < 0:
            raise ValueError("Width must be a postivie number")
        init_vals = {
            "Location": location,
            "Color": color,
            "IsTransparent": transparent,
            "ShadowWidth": round(width * 100),
        }
        super().__init__(**init_vals)

    # endregion init

    # region methods
    def __eq__(self, other: object) -> bool:
        s2: ShadowFormat = None
        if isinstance(other, Shadow):
            s2 = other.get_shadow_format()
        elif getattr(other, "typeName", None) == "com.sun.star.table.ShadowFormat":
            s2 = other
        if s2:
            s1 = self.get_shadow_format()
            return (
                s1.Color == s2.Color
                and s1.IsTransparent == s2.IsTransparent
                and s1.Location == s2.Location
                and s1.ShadowWidth == s2.ShadowWidth
            )
        return False

    def get_shadow_format(self) -> ShadowFormat:
        """
        Gets Shadow format for instance.

        Returns:
            ShadowFormat: Shadow Format
        """
        return ShadowFormat(
            Location=self._get("Location"),
            ShadowWidth=self._get("ShadowWidth"),
            IsTransparent=self._get("IsTransparent"),
            Color=self._get("Color"),
        )

    def _supported_services(self) -> Tuple[str, ...]:
        return ()

    # region apply()

    @overload
    def apply(self, obj: object) -> None:
        ...

    @overload
    def apply(self, obj: object, keys: Dict[str, str]) -> None:
        ...

    def apply(self, obj: object, **kwargs) -> None:
        """
        Applies style to object

        Args:
            obj (object): Object that contains a ``ShadowFormat`` property.
            keys: (Dict[str, str], optional): key map for properties.
                Can be ``prop`` which defaults to ``ShadowFormat``.

        :events:
            .. cssclass:: lo_event

                - :py:attr:`~.events.format_named_event.FormatNamedEvent.STYLE_APPLYING` :eventref:`src-docs-event-cancel`
                - :py:attr:`~.events.format_named_event.FormatNamedEvent.STYLE_APPLYED` :eventref:`src-docs-event`

        Returns:
            None:
        """
        keys = {"prop": "ShadowFormat"}
        if "keys" in kwargs:
            keys.update(kwargs["keys"])

        cargs = CancelEventArgs(source=f"{self.apply.__qualname__}")
        cargs.event_data = self
        self.on_applying(cargs)
        if cargs.cancel:
            return
        _Events().trigger(FormatNamedEvent.STYLE_APPLYING, cargs)
        if cargs.cancel:
            return

        shadow = self.get_shadow_format()
        mProps.Props.set(obj, **{keys["prop"]: shadow})
        eargs = EventArgs.from_args(cargs)
        self.on_applied(eargs)
        _Events().trigger(FormatNamedEvent.STYLE_APPLIED, eargs)

    # endregion apply()

    @staticmethod
    def from_obj(obj: object, prop_name: str) -> Shadow:
        """
        Gets instance from object

        Args:
            obj (object): UNO object
            prop_name (str): Name of property that has a ``ShadowFormat`` value.

        Returns:
            Shadow: Instance from object
        """
        inst = Shadow.empty.copy()

        shadow = cast(ShadowFormat, mProps.Props.get(obj, prop_name))
        if shadow is None:
            return inst
        inst._set("Location", shadow.Location)
        inst._set("Color", shadow.Color)
        inst._set("IsTransparent", shadow.IsTransparent)
        inst._set("ShadowWidth", shadow.ShadowWidth)
        return inst

    @staticmethod
    def from_shadow(shadow: ShadowFormat) -> Shadow:
        """
        Gets an instance

        Args:
            shadow (ShadowFormat): Shadow Format

        Returns:
            Shadow: Instance representing ``shadow``.
        """
        inst = Shadow.empty.copy()
        inst._set("Location", shadow.Location)
        inst._set("Color", shadow.Color)
        inst._set("IsTransparent", shadow.IsTransparent)
        inst._set("ShadowWidth", shadow.ShadowWidth)
        return inst

    # endregion methods

    # region style methods
    def fmt_location(self, value: ShadowLocation) -> Shadow:
        """
        Gets a copy of instance with location set

        Args:
            value (ShadowLocation): Shadow location value

        Returns:
            Shadow: Shadow with location set
        """
        cp = self.copy()
        cp.prop_location = value
        return cp

    def fmt_color(self, value: Color) -> Shadow:
        """
        Gets a copy of instance with color set

        Args:
            value (Color): color value

        Returns:
            Shadow: Shadow with color set
        """
        cp = self.copy()
        cp.prop_color = value
        return cp

    def fmt_transparent(self, value: bool) -> Shadow:
        """
        Gets a copy of instance with transparency set

        Args:
            value (bool): transparency value

        Returns:
            Shadow: Shadow with transparency set
        """
        cp = self.copy()
        cp.prop_transparent = value
        return cp

    def fmt_width(self, value: float) -> Shadow:
        """
        Gets a copy of instance with width set

        Args:
            value (float): width value

        Returns:
            Shadow: Shadow with width set
        """
        cp = self.copy()
        cp.prop_width = value
        return cp

    # endregion style methods

    # region Properties
    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        return FormatKind.STRUCT

    @property
    def prop_location(self) -> ShadowLocation:
        """Gets the location of the shadow."""
        return self._get("Location")

    @prop_location.setter
    def prop_location(self, value: ShadowLocation) -> None:
        self._set("Location", value)

    @property
    def prop_color(self) -> Color:
        """Gets the color value of the shadow."""
        return self._get("Color")

    @prop_color.setter
    def prop_color(self, value: Color) -> None:
        self._set("Color", value)

    @property
    def prop_transparent(self) -> bool:
        """Gets transparent value"""
        return self._get("IsTransparent")

    @prop_transparent.setter
    def prop_transparent(self, value: bool) -> None:
        self._set("IsTransparent", value)

    @property
    def prop_width(self) -> float:
        """Gets the size of the shadow (in mm units)"""
        pv = cast(int, self._get("ShadowWidth"))
        if pv == 0:
            return 0.0
        return float(pv / 100)

    @prop_width.setter
    def prop_width(self, value: float) -> None:
        self._set("ShadowWidth", round(value * 100))

    @static_prop
    def empty() -> Shadow:  # type: ignore[misc]
        """Gets empty Shadow. Static Property. when style is applied it remove any shadow."""
        if Shadow._EMPTY is None:
            Shadow._EMPTY = Shadow(location=ShadowLocation.NONE, transparent=False, color=8421504)
            # just to be exact due to float conversions.
            Shadow._EMPTY._set("ShadowWidth", 176)
        return Shadow._EMPTY

    # endregion Properties
