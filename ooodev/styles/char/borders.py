"""
Module for managing character borders.

.. versionadded:: 0.9.0
"""
# region imports
from __future__ import annotations
from typing import Tuple

import uno
from ...exceptions import ex as mEx
from ...meta.static_prop import static_prop
from ...utils import info as mInfo
from ...utils import lo as mLo
from ..style_base import StyleBase

from ..structs import side
from ..structs import shadow
from ..structs import border_table
from . import padding
from ..structs.side import Side as Side, SideFlags as SideFlags
from ..structs.shadow import Shadow
from .padding import Padding as Padding
from . import sides
from .sides import Sides

from ooo.dyn.table.border_line import BorderLine as BorderLine
from ooo.dyn.table.border_line_style import BorderLineStyleEnum as BorderLineStyleEnum
from ooo.dyn.table.border_line2 import BorderLine2 as BorderLine2
from ooo.dyn.table.shadow_format import ShadowFormat as ShadowFormat
from ooo.dyn.table.shadow_location import ShadowLocation as ShadowLocation


# endregion imports


class Borders(StyleBase):
    """
    Border used in styles for characters.

    All methods starting with ``style_`` can be used to chain together Borders properties.

    .. versionadded:: 0.9.0
    """

    _DEFAULT = None
    _EMPTY = None

    # region init

    def __init__(
        self,
        *,
        right: Side | None = None,
        left: Side | None = None,
        top: Side | None = None,
        bottom: Side | None = None,
        border_side: Side | None = None,
        shadow: Shadow | None = None,
        padding: Padding | None = None,
    ) -> None:
        """
        _summary_

        Args:
            left (Side | None, optional): Determines the line style at the left edge.
            right (Side | None, optional): Determines the line style at the right edge.
            top (Side | None, optional): Determines the line style at the top edge.
            bottom (Side | None, optional): Determines the line style at the bottom edge.
            border_side (Side | None, optional): Determines the line style at the top, bottom, left, right edges. If this argument has a value then arguments ``top``, ``bottom``, ``left``, ``right`` are ignored
            shadow (Shadow | None, optional): Character Shadow
            padding (BorderPadding | None, optional): Character padding
        """
        init_vals = {}

        if not shadow is None:
            init_vals["CharShadowFormat"] = shadow.get_shadow_format()

        sides = Sides(
            left=left,
            right=right,
            top=top,
            bottom=bottom,
            border_side=border_side,
        )

        if sides.has_attribs:
            self._sides = sides
        else:
            self._sides = None
        self._padding = padding

        super().__init__(**init_vals)

    # endregion init

    # region Style Methods
    def style_border_side(self, value: Side | None) -> Borders:
        """
        Gets copy of instance with left, right, top, bottom sides set or removed

        Args:
            value (Side | None): Side value

        Returns:
            Borders: Borders instance
        """
        cp = self.copy()
        if cp._sides is None and value is None:
            return cp
        if cp._sides is None:
            cp._sides = Sides(border_side=value)
            return cp
        sides = cp._sides.copy()
        sides.prop_left = value
        sides.prop_right = value
        sides.prop_top = value
        sides.prop_bottom = value
        cp._sides = sides
        return cp

    def style_left(self, value: Side | None) -> Borders:
        """
        Gets copy of instance with left set or removed

        Args:
            value (Side | None): Side value

        Returns:
            Borders: Borders instance
        """
        cp = self.copy()
        if cp._sides is None and value is None:
            return cp
        if cp._sides is None:
            cp._sides = Sides(left=value)
            return cp
        sides = cp._sides.copy()
        sides.prop_left = value
        cp._sides = sides
        return cp

    def style_right(self, value: Side | None) -> Borders:
        """
        Gets copy of instance with right set or removed

        Args:
            value (Side | None): Side value

        Returns:
            Borders: Borders instance
        """
        cp = self.copy()
        if cp._sides is None and value is None:
            return cp
        if cp._sides is None:
            cp._sides = Sides(right=value)
            return cp
        sides = cp._sides.copy()
        sides.prop_right = value
        cp._sides = sides
        return cp

    def style_top(self, value: Side | None) -> Borders:
        """
        Gets copy of instance with top set or removed

        Args:
            value (Side | None): Side value

        Returns:
            Borders: Borders instance
        """
        cp = self.copy()
        if cp._sides is None and value is None:
            return cp
        if cp._sides is None:
            cp._sides = Sides(top=value)
            return cp
        sides = cp._sides.copy()
        sides.prop_top = value
        cp._sides = sides
        return cp

    def style_bottom(self, value: Side | None) -> Borders:
        """
        Gets copy of instance with bottom set or removed

        Args:
            value (Side | None): Side value

        Returns:
            Borders: Borders instance
        """
        cp = self.copy()
        if cp._sides is None and value is None:
            return cp
        if cp._sides is None:
            cp._sides = Sides(bottom=value)
            return cp
        sides = cp._sides.copy()
        sides.prop_bottom = value
        cp._sides = sides
        return cp

    def style_shadow(self, value: Shadow | None) -> Borders:
        """
        Gets copy of instance with shadow set or removed

        Args:
            value (Shadow | None): Shadow value

        Returns:
            Borders: Borders instance
        """
        cp = self.copy()
        if value is None:
            cp._remove("CharShadowFormat")
        else:
            cp._set("CharShadowFormat", value.get_shadow_format())
        return cp

    def style_padding(self, value: Padding | None) -> Borders:
        """
        Gets copy of instance with padding set or removed

        Args:
            value (Padding | None): Padding value

        Returns:
            Borders: Borders instance
        """
        cp = self.copy()
        cp._padding = value
        return cp

    # endregion Style Methods

    # region methods

    def apply_style(self, obj: object, **kwargs) -> None:
        """
        Applies padding to ``obj``

        Args:
            obj (object): Object that supports ``com.sun.star.style.CharacterProperties`` service.
            kwargs (Any, optional): Expandable list of key value pairs that may be used in child classes.

        Returns:
            None:
        """
        if not self._padding is None:
            self._padding.apply_style(obj)
        if not self._sides is None:
            self._sides.apply_style(obj)
        if mInfo.Info.support_service(obj, "com.sun.star.style.CharacterProperties"):
            try:
                super().apply_style(obj)
            except mEx.MultiError as e:
                mLo.Lo.print(f"{self.__name__}.apply_style(): Unable to set Property")
                for err in e.errors:
                    mLo.Lo.print(f"  {err}")

    def get_attrs(self) -> Tuple[str, ...]:
        """
        Gets the attributes that are slated for change in the current instance

        Returns:
            Tuple(str, ...): Tuple of attribures
        """
        # get current keys in internal dictionary
        attribs = set(super().get_attrs())
        if self._padding:
            attribs.update(self._padding.get_attrs())
        if self._sides:
            attribs.update(self._sides.get_attrs())
        return tuple(attribs)

    def copy(self) -> Borders:
        """
        Creates a copy

        Returns:
            Borders: Copy of instance
        """
        cp = super().copy()
        if self._sides is None:
            cp._sides = None
        else:
            cp._sides = self._sides.copy()
        if self._padding is None:
            cp._padding = None
        else:
            cp._padding = self._padding.copy()
        return cp

    # endregion methods

    # region Properties
    @property
    def has_attribs(self) -> bool:
        """Gets If instantance has any attributes set."""
        if self._dv:
            return True
        if self._padding:
            return True
        if self._sides:
            return True
        return False

    @static_prop
    def default(cls) -> Borders:
        """Gets Default Border. Static Property"""
        if cls._DEFAULT is None:
            cls._DEFAULT = Borders(border_side=Side.empty, padding=Padding.default, shadow=Shadow.empty)
        return cls._DEFAULT

    @static_prop
    def empty(cls) -> Borders:
        """Gets Empty Border. Static Property. When style is applied formatting is removed."""
        if cls._EMPTY is None:
            cls._EMPTY = Borders(
                border_side=Side.empty,
                vertical=Side.empty,
                horizontal=Side.empty,
                shadow=Shadow.empty,
                padding=Padding.default,
            )
        return cls._EMPTY

    # endregion Properties