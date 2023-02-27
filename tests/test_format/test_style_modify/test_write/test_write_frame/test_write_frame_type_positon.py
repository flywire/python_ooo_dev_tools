from __future__ import annotations
import pytest

if __name__ == "__main__":
    pytest.main([__file__])

import uno
from ooodev.format.writer.modify.frame.type import (
    StyleFrameKind,
    Position,
    HoriOrient,
    VertOrient,
    Horizontal,
    Vertical,
    RelHoriOrient,
    RelVertOrient,
)
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
        GUI.zoom(GUI.ZoomEnum.ENTIRE_PAGE)
    try:
        cursor = Write.get_cursor(doc)
        if not Lo.bridge_connector.headless:
            Write.append_para(cursor=cursor, text=para_text)

        style = Position(
            horizontal=Horizontal(position=HoriOrient.CENTER, rel=RelHoriOrient.LEFT_PARAGRAPH_BORDER),
            vertical=Vertical(position=VertOrient.CENTER, rel=RelVertOrient.PAGE_TEXT_AREA),
            mirror_even=False,
            keep_boundries=False,
            style_name=StyleFrameKind.FRAME,
        )

        style.apply(doc)
        # props = style.get_style_props(doc)

        f_style = Position.from_style(doc, style.prop_style_name)
        assert f_style.prop_inner.prop_horizontal == style.prop_inner.prop_horizontal
        assert f_style.prop_inner.prop_vertical == style.prop_inner.prop_vertical
        assert f_style.prop_inner.prop_mirror_even == style.prop_inner.prop_mirror_even
        assert f_style.prop_inner.prop_keep_boundries == style.prop_inner.prop_keep_boundries

        style = Position(
            horizontal=Horizontal(position=HoriOrient.LEFT_OR_INSIDE, rel=RelHoriOrient.ENTIRE_PAGE),
            vertical=Vertical(position=VertOrient.BOTTOM, rel=RelVertOrient.MARGIN),
            mirror_even=True,
            keep_boundries=True,
            style_name=StyleFrameKind.FRAME,
        )

        style.apply(doc)
        f_style = Position.from_style(doc, style.prop_style_name)
        assert f_style.prop_inner.prop_horizontal == style.prop_inner.prop_horizontal
        assert f_style.prop_inner.prop_vertical == style.prop_inner.prop_vertical
        assert f_style.prop_inner.prop_mirror_even == style.prop_inner.prop_mirror_even
        assert f_style.prop_inner.prop_keep_boundries == style.prop_inner.prop_keep_boundries

        style = Position(
            horizontal=Horizontal(position=HoriOrient.FROM_LEFT_OR_INSIDE, rel=RelHoriOrient.ENTIRE_PAGE, amount=7.8),
            vertical=Vertical(position=VertOrient.FROM_TOP_OR_BOTTOM, rel=RelVertOrient.MARGIN, amount=3.6),
            mirror_even=False,
            keep_boundries=False,
            style_name=StyleFrameKind.FRAME,
        )

        style.apply(doc)
        f_style = Position.from_style(doc, style.prop_style_name)
        assert f_style.prop_inner.prop_horizontal == style.prop_inner.prop_horizontal
        assert f_style.prop_inner.prop_vertical == style.prop_inner.prop_vertical
        assert f_style.prop_inner.prop_mirror_even == style.prop_inner.prop_mirror_even
        assert f_style.prop_inner.prop_keep_boundries == style.prop_inner.prop_keep_boundries

        Lo.delay(delay)
    finally:
        Lo.close_doc(doc)