from __future__ import annotations
from typing import cast, Type, TypeVar
import uno
from ooo.dyn.drawing.hatch_style import HatchStyle as HatchStyle

from ...page_style_base_multi import PageStyleBaseMulti
from ......utils.color import Color
from ......utils.data_type.angle import Angle as Angle
from ......utils.data_type.color_range import ColorRange as ColorRange
from ......utils.data_type.intensity import Intensity as Intensity
from ......utils.data_type.intensity_range import IntensityRange as IntensityRange
from ......utils.data_type.offset import Offset as Offset
from .....writer.style.page.kind.style_page_kind import StylePageKind as StylePageKind
from .....preset.preset_hatch import PresetHatchKind as PresetHatchKind
from .....direct.common.props.area_hatch_props import AreaHatchProps
from .....direct.fill.area.hatch import Hatch as InnerHatch

_THatch = TypeVar(name="_THatch", bound="Hatch")


class Hatch(PageStyleBaseMulti):
    """
    Page Footer Hatch
    .. versionadded:: 0.9.0
    """

    def __init__(
        self,
        *,
        style: HatchStyle = HatchStyle.SINGLE,
        color: Color = Color(0),
        space: float = 0.0,
        angle: Angle | int = 0,
        bg_color: Color = Color(-1),
        style_name: StylePageKind | str = StylePageKind.STANDARD,
        style_family: str = "PageStyles",
    ) -> None:
        """
        Constructor

        Args:
            style (HatchStyle, optional): Specifies the kind of lines used to draw this hatch. Default ``HatchStyle.SINGLE``.
            color (Color, optional): Specifies the color of the hatch lines. Default ``0``.
            space (int, optional): Specifies the space between the lines in the hatch (in ``mm`` units). Default ``0.0``
            angle (Angle, int, optional): Specifies angle of the hatch in degrees. Default to ``0``.
            bg_color(Color, optionl): Specifies the background Color. Set this ``-1`` (default) for no background color.
            style_name (StyleParaKind, str, optional): Specifies the Page Style that instance applies to. Deftult is Default Page Style.
            style_family (str, optional): Style family. Defatult ``PageStyles``.

        Returns:
            None:
        """

        direct = InnerHatch(
            style=style,
            color=color,
            space=space,
            angle=angle,
            bg_color=bg_color,
            _cattribs=self._get_inner_cattribs(),
        )
        super().__init__()
        self._style_name = str(style_name)
        self._style_family_name = style_family
        self._set_style("direct", direct, *direct.get_attrs())

    # region internal methods
    def _get_inner_props(self) -> AreaHatchProps:
        return AreaHatchProps(
            color="HeaderFillColor",
            style="HeaderFillStyle",
            bg="HeaderFillBackground",
            hatch_prop="HeaderFillHatch",
        )

    def _get_inner_cattribs(self) -> dict:
        return {
            "_supported_services_values": self._supported_services(),
            "_format_kind_prop": self.prop_format_kind,
            "_props_internal_attributes": self._get_inner_props(),
        }

    # endregion internal methods

    # region Static methods
    @classmethod
    def from_style(
        cls: Type[_THatch],
        doc: object,
        style_name: StylePageKind | str = StylePageKind.STANDARD,
        style_family: str = "PageStyles",
    ) -> _THatch:
        """
        Gets instance from Document.

        Args:
            doc (object): UNO Documnet Object.
            style_name (StyleParaKind, str, optional): Specifies the Paragraph Style that instance applies to. Deftult is Default Paragraph Style.
            style_family (str, optional): Style family. Defatult ``PageStyles``.

        Returns:
            Hatch: ``Hatch`` instance from document properties.
        """
        inst = cls(style_name=style_name, style_family=style_family)
        direct = InnerHatch.from_obj(inst.get_style_props(doc), _cattribs=inst._get_inner_cattribs())
        inst._set_style("direct", direct, *direct.get_attrs())
        return inst

    @classmethod
    def from_preset(
        cls: Type[_THatch],
        preset: PresetHatchKind,
        style_name: StylePageKind | str = StylePageKind.STANDARD,
        style_family: str = "PageStyles",
    ) -> _THatch:
        """
        Gets instance from preset.

        Args:
            preset (PresetKind): Preset.
            style_name (StyleParaKind, str, optional): Specifies the Paragraph Style that instance applies to. Deftult is Default Paragraph Style.
            style_family (str, optional): Style family. Defatult ``PageStyles``.

        Returns:
            Gradient: ``Gradient`` instance from preset.
        """
        inst = cls(style_name=style_name, style_family=style_family)
        direct = InnerHatch.from_preset(preset=preset, _cattribs=inst._get_inner_cattribs())
        inst._set_style("direct", direct, *direct.get_attrs())
        return inst

    # endregion Static methods

    # region Properties
    @property
    def prop_style_name(self) -> str:
        """Gets/Sets property Style Name"""
        return self._style_name

    @prop_style_name.setter
    def prop_style_name(self, value: str | StylePageKind):
        self._style_name = str(value)

    @property
    def prop_inner(self) -> InnerHatch:
        """Gets/Sets Inner Hatch instance"""
        try:
            return self._direct_inner
        except AttributeError:
            self._direct_inner = cast(InnerHatch, self._get_style_inst("direct"))
        return self._direct_inner

    @prop_inner.setter
    def prop_inner(self, value: InnerHatch) -> None:
        if not isinstance(value, InnerHatch):
            raise TypeError(f'Expected type of InnerHatch, got "{type(value).__name__}"')
        self._del_attribs("_direct_inner")
        self._set_style("direct", value, *value.get_attrs())

    # endregion Properties