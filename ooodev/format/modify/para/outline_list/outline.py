from __future__ import annotations
from typing import cast
import uno
from ....writer.style.para.kind import StyleParaKind as StyleParaKind
from ....writer.style.char.kind import StyleCharKind as StyleCharKind
from ..para_style_base_multi import ParaStyleBaseMulti
from ....direct.para.outline_list.outline import Outline as DirectOutline, LevelKind as LevelKind


class Outline(ParaStyleBaseMulti):
    """
    Paragraph Style Outline

    .. versionadded:: 0.9.0
    """

    def __init__(
        self,
        *,
        level: LevelKind = LevelKind.TEXT_BODY,
        style_name: StyleParaKind | str = StyleParaKind.STANDARD,
        style_family: str = "ParagraphStyles",
    ) -> None:
        """
        Constructor

        Args:
            level (LevelKind): Outline level.
            style_name (StyleParaKind, str, optional): Specifies the Paragraph Style that instance applies to. Deftult is Default Paragraph Style.
            style_family (str, optional): Style family. Defatult ``ParagraphStyles``.

        Returns:
            None:
        """

        direct = DirectOutline(level=level)
        super().__init__()
        self._style_name = str(style_name)
        self._style_family_name = style_family
        self._set_style("direct", direct, *direct.get_attrs())

    @classmethod
    def from_style(
        cls,
        doc: object,
        style_name: StyleParaKind | str = StyleParaKind.STANDARD,
        style_family: str = "ParagraphStyles",
    ) -> Outline:
        """
        Gets instance from Document.

        Args:
            doc (object): UNO Documnet Object.
            style_name (StyleParaKind, str, optional): Specifies the Paragraph Style that instance applies to. Deftult is Default Paragraph Style.
            style_family (str, optional): Style family. Defatult ``ParagraphStyles``.

        Returns:
            Outline: ``Outline`` instance from document properties.
        """
        inst = super(Outline, cls).__new__(cls)
        inst.__init__(style_name=style_name, style_family=style_family)
        direct = DirectOutline.from_obj(inst.get_style_props(doc))
        inst._set_style("direct", direct, *direct.get_attrs())
        return inst

    @property
    def prop_style_name(self) -> str:
        """Gets/Sets property Style Name"""
        return self._style_name

    @prop_style_name.setter
    def prop_style_name(self, value: str | StyleParaKind):
        self._style_name = str(value)

    @property
    def prop_inner(self) -> DirectOutline:
        """Gets Inner Outline instance"""
        try:
            return self._direct_inner
        except AttributeError:
            self._direct_inner = cast(DirectOutline, self._get_style_inst("direct"))
        return self._direct_inner
