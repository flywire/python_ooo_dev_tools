from __future__ import annotations
from typing import cast
from enum import Enum

from ..exceptions import ex as mEx
from ..utils import info as mInfo
from ..utils import lo as mLo
from ..utils.color import Color
from .style_base import StyleBase

from ooo.dyn.awt.char_set import CharSetEnum as CharSetKind
from ooo.dyn.awt.font_family import FontFamilyEnum as FamilyKind
from ooo.dyn.awt.font_slant import FontSlant as SlantKind
from ooo.dyn.awt.font_strikeout import FontStrikeoutEnum as StrikeOutKind
from ooo.dyn.awt.font_underline import FontUnderlineEnum as LineKind
from ooo.dyn.awt.font_weight import FontWeightEnum as WeightKind


class CharSpacingKind(float, Enum):
    """Character Spacing"""

    VERY_TIGHT = -3.0
    TIGHT = -1.5
    NORMAL = 0.0
    LOOSE = 3.0
    VERY_LOOSE = 6.0


class Font(StyleBase):
    POINT_RATIO = 35.28
    """Ratio multiplier to convert from point to CharKerning"""

    def __init__(
        self,
        *,
        b: bool | None = None,
        i: bool | None = None,
        u: bool | None = None,
        bg_color: Color | None = None,
        bg_transparent: bool | None = None,
        charset: CharSetKind | None = None,
        color: Color | None = None,
        family: FamilyKind | None = None,
        height: float | None = None,
        name: str | None = None,
        overline: LineKind | None = None,
        overline_color: Color | None = None,
        rotation: float | None = None,
        slant: SlantKind | None = None,
        spacing: CharSpacingKind | float | None = None,
        strike: StrikeOutKind | None = None,
        sub_script: bool | None = None,
        super_script: bool | None = None,
        underine: LineKind | None = None,
        underine_color: Color | None = None,
        weight: WeightKind | None = None,
        word_mode: bool | None = None,
    ) -> None:
        """
        Font options used in styles.

        Args:
            b (bool, optional): Short cut to set ``weight`` to bold.
            i (bool, optional): Short cut to set ``slant`` to italic.
            u (bool, optional): Short cut ot set ``underline`` to underline.
            bg_color (Color, optional): The value of the text background color.
            bg_transparent (bool, optional): Determines if the text background color is set to transparent.
            charset (CharSetKind, optional): The text encoding of the font.
            color (Color, optional): The value of the text color.
            family (FamilyKind, optional): Font Family
            height (float, optional): This value contains the height of the characters in point.
            name (str, optional): This property specifies the name of the font style. It may contain more than one name separated by comma.
            overline (LineKind, optional): The value for the character overline.
            overline_color (Color, optional): Specifies if the property ``CharOverlinelineColor`` is used for an overline.
            rotation (float, optional): Determines the rotation of a character in degrees. Depending on the implementation only certain values may be allowed.
            slant (SlantKind, optional): The value of the posture of the document such as ``SlantKind.ITALIC``.
            spacing(CharSpacingKind, float, optional): Character spacing in point units.
            strike (StrikeOutKind, optional): Dermines the type of the strike out of the character.
            sub_script (bool, optional): Sub script option.
            super_script (bool, optional): Super script option.
            underine (LineKind, optional): The value for the character underline.
            underine_color (Color, optional): Specifies if the property ``CharUnderlineColor`` is used for an underline.
            weight (WeightKind, optional): The value of the font weight.
            word_mode(bool, optional): If ``True``, the underline and strike-through properties are not applied to white spaces.
        """
        # could not find any documention in the API or elsewhere online for Overline
        # see: https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1CharacterProperties.html
        init_vals = {
            "FontName": name,
            "CharColor": color,
            "CharBackColor": bg_color,
            "CharUnderlineColor": underine_color,
            "CharOverlineColor": overline_color,
            "CharHeight": height,
            "CharBackTransparent": bg_transparent,
            "CharWordMode": word_mode,
        }
        if not bg_color is None:
            init_vals["CharBackTransparent"] = False

        if not overline_color is None:
            init_vals["CharOverlineHasColor"] = True
        if not underine_color is None:
            init_vals["CharUnderlineHasColor"] = True
        if not charset is None:
            init_vals["CharFontCharSet"] = charset.value
        if not family is None:
            init_vals["CharFontFamily"] = family.value
        if not strike is None:
            init_vals["CharStrikeout"] = strike.value

        if not b is None:
            if b:
                init_vals["CharWeight"] = WeightKind.BOLD.value
            else:
                init_vals["CharWeight"] = WeightKind.NORMAL.value
        if not i is None:
            if i:
                init_vals["CharPosture"] = SlantKind.ITALIC
            else:
                init_vals["CharWeight"] = SlantKind.NONE
        if not u is None:
            if u:
                init_vals["CharUnderline"] = LineKind.SINGLE.value
            else:
                init_vals["CharUnderline"] = LineKind.NONE.value

        if not overline is None:
            init_vals["CharOverline"] = overline.value

        if not underine is None:
            init_vals["CharUnderline"] = underine.value

        if not weight is None:
            init_vals["CharWeight"] = weight.value

        if not slant is None:
            init_vals["CharPosture"] = slant

        if not spacing is None:
            init_vals["CharKerning"] = round(float(spacing) * Font.POINT_RATIO)

        if not super_script is None:
            if super_script:
                init_vals["CharEscapementHeight"] = 58
                init_vals["CharEscapement"] = 14_000
            else:
                init_vals["CharEscapementHeight"] = 100
                init_vals["CharEscapement"] = 0

        if not sub_script is None:
            if sub_script:
                init_vals["CharEscapementHeight"] = 58
                init_vals["CharEscapement"] = -14_000
            else:
                init_vals["CharEscapementHeight"] = 100
                init_vals["CharEscapement"] = 0

        if not rotation is None:
            init_vals["CharRotation"] = round(rotation * 10)

        super().__init__(**init_vals)

    def apply_style(self, obj: object) -> None:
        if mInfo.Info.support_service(obj, "com.sun.star.style.CharacterProperties"):
            try:
                super().apply_style(obj)
            except mEx.MultiError as e:
                mLo.Lo.print(f"Unable to set Property:")
                for err in e.errors:
                    mLo.Lo.print(f"  {err}")
        else:
            mLo.Lo.print("Unable to apply font style. CharacterProperties service not supported")

    @property
    def b(self) -> bool:
        """Specifies bold"""
        pv = cast(float, self._get("CharWeight"))
        if not pv is None:
            return pv == WeightKind.BOLD.value
        return False

    @property
    def bg_color(self) -> Color | None:
        """This property contains the text background color."""
        return self._get("CharBackColor")

    @property
    def bg_color_transparent(self) -> bool | None:
        """This property contains the text background color."""
        return self._get("CharBackTransparent")

    @property
    def i(self) -> bool | None:
        """Specifies italic"""
        pv = cast(SlantKind, self._get("CharPosture"))
        if not pv is None:
            return pv == SlantKind.ITALIC
        return None

    @property
    def u(self) -> bool | None:
        """Specifies underline"""
        pv = cast(int, self._get("CharUnderline"))
        if not pv is None:
            return pv != LineKind.NONE.value
        return None

    @property
    def charset(self) -> CharSetKind | None:
        """This property contains the text encoding of the font."""
        pv = cast(int, self._get("CharFontCharSet"))
        if not pv is None:
            return CharSetKind(pv)
        return None

    @property
    def color(self) -> Color | None:
        """This property contains the value of the text color."""
        return self._get("CharColor")

    @property
    def family(self) -> FamilyKind | None:
        """This property contains font family."""
        pv = cast(FamilyKind, self._get("CharFontFamily"))
        if not pv is None:
            return FamilyKind(pv)
        return None

    @property
    def height(self) -> float | None:
        """This value contains the height of the characters in point."""
        return self._get("CharHeight")

    @property
    def name(self) -> str | None:
        """This property specifies the name of the font style. It may contain more than one name separated by comma."""
        return self._get("FontName")

    @property
    def strike(self) -> StrikeOutKind | None:
        """This property determines the type of the strike out of the character."""
        pv = cast(int, self._get("CharStrikeout"))
        if not pv is None:
            return StrikeOutKind(pv)
        return None

    @property
    def weight(self) -> WeightKind | None:
        """This property contains the value of the font weight."""
        pv = cast(float, self._get("CharWeight"))
        if not pv is None:
            return WeightKind(pv)
        return None

    @property
    def slant(self) -> SlantKind | None:
        """This property contains the value of the posture of the document such as  ``SlantKind.ITALIC``"""
        return self._get("CharPosture")

    @property
    def spacing(self) -> float | None:
        """This value contains character spacing in point units"""
        pv = self._get("CharKerning")
        if not pv is None:
            if pv == 0.0:
                return 0.0
            return pv / Font.POINT_RATIO
        return None

    @property
    def super_script(self) -> bool | None:
        pv = cast(int, self._get("CharEscapement"))
        if not pv is None:
            return pv > 0
        return None

    @property
    def sub_script(self) -> bool | None:
        pv = cast(int, self._get("CharEscapement"))
        if not pv is None:
            return pv < 0
        return None

    @property
    def overline(self) -> LineKind | None:
        """This property contains the value for the character overline."""
        pv = cast(int, self._get("CharOverline"))
        if not pv is None:
            return LineKind(pv)
        return None

    @property
    def overline_color(self) -> Color | None:
        """This property specifies if the property ``CharOverlineColor`` is used for an underline."""
        return self._get("CharOverlineColor")

    @property
    def underline(self) -> LineKind | None:
        """This property contains the value for the character underline."""
        pv = cast(int, self._get("CharUnderline"))
        if not pv is None:
            return LineKind(pv)
        return None

    @property
    def underine_color(self) -> Color | None:
        """This property specifies if the property ``CharUnderlineColor`` is used for an underline."""
        return self._get("CharUnderlineColor")

    @property
    def rotation(self) -> float | None:
        """
        This optional property determines the rotation of a character in degrees.

        Depending on the implementation only certain values may be allowed.
        """
        pv = cast(int, self._get("CharRotation"))
        if not pv is None:
            return float(pv / 10)
        return None

    @property
    def word_mode(self) -> bool | None:
        """If this property is ``True``, the underline and strike-through properties are not applied to white spaces."""
        return self._get("CharWordMode")
