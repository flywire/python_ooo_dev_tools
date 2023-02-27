from __future__ import annotations
import pytest

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.format.writer.modify.char.borders import Padding
from ooodev.utils.gui import GUI
from ooodev.utils.lo import Lo
from ooodev.office.write import Write


def test_write(loader, para_text) -> None:
    # delay = 0 if Lo.bridge_connector.headless else 3_000
    delay = 0

    doc = Write.create_doc()
    if not Lo.bridge_connector.headless:
        GUI.set_visible()
        Lo.delay(500)
        GUI.zoom(GUI.ZoomEnum.ZOOM_150_PERCENT)
    try:
        cursor = Write.get_cursor(doc)
        Write.append_para(cursor=cursor, text=para_text)

        style = Padding(padding_all=3.0)
        style.apply(doc)
        props = style.get_style_props(doc)
        assert props.getPropertyValue("CharLeftBorderDistance") in (298, 299, 300, 301, 302)

        f_style = Padding.from_style(doc)
        assert f_style.prop_inner.prop_left == pytest.approx(3.0, rel=1e2)
        assert f_style.prop_inner.prop_top == pytest.approx(3.0, rel=1e2)
        assert f_style.prop_inner.prop_right == pytest.approx(3.0, rel=1e2)
        assert f_style.prop_inner.prop_bottom == pytest.approx(3.0, rel=1e2)

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)