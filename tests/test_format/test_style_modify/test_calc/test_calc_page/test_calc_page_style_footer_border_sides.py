from __future__ import annotations
import pytest

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.format.calc.modify.page.footer import Footer, CalcStylePageKind
from ooodev.format.calc.modify.page.footer.borders import (
    Sides,
    Side,
    LineSize,
    BorderLineKind,
)
from ooodev.format import Styler
from ooodev.utils.gui import GUI
from ooodev.utils.lo import Lo
from ooodev.utils.color import StandardColor
from ooodev.office.calc import Calc
from ooodev.utils.data_type.unit_mm100 import UnitMM100


def test_calc(loader) -> None:
    # delay = 0 if Lo.bridge_connector.headless else 3_000
    delay = 0

    doc = Calc.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        sheet = Calc.get_active_sheet()

        cell_obj = Calc.get_cell_obj("A1")
        Calc.set_val(value="Hello", sheet=sheet, cell_obj=cell_obj)

        footer_style = Footer(
            on=True,
            shared_first=True,
            shared=True,
            height=10.0,
            spacing=3.0,
            spacing_dyn=True,
            margin_left=1.5,
            margin_right=2.0,
        )
        width100 = UnitMM100.from_pt(float(LineSize.MEDIUM))
        side = Side(line=BorderLineKind.DOUBLE, color=StandardColor.RED_DARK3, width=width100)

        style = Sides(all=side, style_name=CalcStylePageKind.DEFAULT)
        Styler.apply(doc, footer_style, style)
        # props = style.get_style_props(doc)

        f_style = Sides.from_style(doc, style.prop_style_name)
        f_side = f_style.prop_inner.prop_left
        assert f_side.prop_color == side.prop_color
        assert f_side.prop_width.get_value_mm100() in range(width100.value - 2, width100.value + 3)  # +- 2

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)
