from __future__ import annotations
from typing import cast
import pytest

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.format.calc.style import Page, CalcStylePageKind
from ooodev.utils.gui import GUI
from ooodev.utils.lo import Lo
from ooodev.office.calc import Calc
from ooodev.utils.color import CommonColor


def test_calc(loader) -> None:
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

        style = Page(name=CalcStylePageKind.DEFAULT)
        style.apply(sheet)

        f_style = Page.from_obj(sheet)
        assert f_style.prop_name == style.prop_name

        # ==============================================
        style = Page().report
        style.apply(sheet)

        f_style = Page.from_obj(sheet)
        assert f_style.prop_name == style.prop_name

        style = Page(name=CalcStylePageKind.DEFAULT)
        xprops = style.get_style_props()
        assert xprops is not None
        xprops.setPropertyValue("BackColor", CommonColor.CORAL)
        val = cast(int, xprops.getPropertyValue("BackColor"))
        assert val == CommonColor.CORAL

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)
