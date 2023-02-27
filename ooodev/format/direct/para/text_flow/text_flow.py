"""
Modele for managing paragraph Text Flow.

.. versionadded:: 0.9.0
"""
from __future__ import annotations
from typing import Tuple, cast, Type, TypeVar, overload

from .....events.args.cancel_event_args import CancelEventArgs
from .....exceptions import ex as mEx
from .....meta.static_prop import static_prop
from ....style_base import StyleMulti
from ....kind.format_kind import FormatKind
from .breaks import Breaks
from .hyphenation import Hyphenation
from .flow_options import FlowOptions

from ooo.dyn.style.break_type import BreakType as BreakType

_TTextFlow = TypeVar(name="_TTextFlow", bound="TextFlow")


class TextFlow(StyleMulti):
    """
    Paragraph Text Flow

    .. versionadded:: 0.9.0
    """

    # region init

    def __init__(
        self,
        *,
        hy_auto: bool | None = None,
        hy_no_caps: bool | None = None,
        hy_start_chars: int | None = None,
        hy_end_chars: int | None = None,
        hy_max: int | None = None,
        bk_type: BreakType | None = None,
        bk_style: str | None = None,
        bk_num: int | None = None,
        op_orphans: int | None = None,
        op_widows: int | None = None,
        op_keep: bool | None = None,
        op_no_split: bool | None = None,
    ) -> None:
        """
        Constructor

        Args:
            hy_auto (bool, optional): Hyphenate automatically.
            hy_no_caps (bool, optional): Don't hyphenate word in caps.
            hy_start_chars (int, optional): Characters at line begin.
            hy_end_chars (int, optional): charactors at line end.
            hy_max (int, optional): Maximum consecutive hyphenated lines.
            bk_type (Any, optional): Break type.
            bk_style (str, optional): Style to apply to break.
            bk_num (int, optional): Page number to apply to break.
            op_orphans (int, optional): Number of Orphan Control Lines.
            op_widows (int, optional): Number Widow Control Lines.
            op_keep (bool, optional): Keep with next paragraph.
            op_no_split (bool, optional): Do not split paragraph.
        Returns:
            None:

        Note:
            Arguments starting with ``hy_`` are for hyphenation

            Arguments starting with ``bk_`` are for Breaks

            Arguments starting with ``op_`` are for Flow options
        """
        # https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1ParagraphProperties-members.html
        init_vals = {}

        hy = Hyphenation(
            auto=hy_auto, no_caps=hy_no_caps, start_chars=hy_start_chars, end_chars=hy_end_chars, max=hy_max
        )

        brk = Breaks(type=bk_type, style=bk_style, num=bk_num)

        flo = FlowOptions(orphans=op_orphans, widows=op_widows, keep=op_keep, no_split=op_no_split)

        super().__init__(**init_vals)
        if hy.prop_has_attribs:
            self._set_style("hyphenation", hy, *hy.get_attrs())
        if brk.prop_has_attribs:
            self._set_style("breaks", brk, *brk.get_attrs())
        if flo.prop_has_attribs:
            self._set_style("flow_options", flo, *flo.get_attrs())

    # endregion init

    # region methods
    def _supported_services(self) -> Tuple[str, ...]:
        try:
            return self._supported_services_values
        except AttributeError:
            self._supported_services_values = (
                "com.sun.star.style.ParagraphProperties",
                "com.sun.star.style.ParagraphStyle",
            )
        return self._supported_services_values

    def _on_modifing(self, event: CancelEventArgs) -> None:
        if self._is_default_inst:
            raise ValueError("Modifying a default instance is not allowed")
        return super()._on_modifing(event)

    # region from_obj()
    @overload
    @classmethod
    def from_obj(cls: Type[_TTextFlow], obj: object) -> _TTextFlow:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_TTextFlow], obj: object, **kwargs) -> _TTextFlow:
        ...

    @classmethod
    def from_obj(cls: Type[_TTextFlow], obj: object, **kwargs) -> _TTextFlow:
        """
        Gets instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            TextFlow: ``TextFlow`` instance that represents ``obj`` Indents and spacing.
        """
        inst = cls(**kwargs)
        if not inst._is_valid_obj(obj):
            raise mEx.NotSupportedError(f'Object is not supported for conversion to "{cls.__name__}"')

        hy = Hyphenation.from_obj(obj)
        if hy.prop_has_attribs:
            inst._set_style("hyphenation", hy, *hy.get_attrs())
        brk = Breaks.from_obj(obj)
        if brk.prop_has_attribs:
            inst._set_style("breaks", brk, *brk.get_attrs())
        flo = FlowOptions.from_obj(obj)
        if flo.prop_has_attribs:
            inst._set_style("flow_options", flo, *flo.get_attrs())
        return inst

    # endregion from_obj()

    # endregion methods

    # region properties
    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        try:
            return self._format_kind_prop
        except AttributeError:
            self._format_kind_prop = FormatKind.PARA
        return self._format_kind_prop

    @property
    def prop_inner_hyphenation(self) -> Hyphenation | None:
        """Gets Hyphenation instance"""
        try:
            return self._direct_inner_hy
        except AttributeError:
            self._direct_inner_hy = cast(Hyphenation, self._get_style_inst("hyphenation"))
        return self._direct_inner_hy

    @property
    def prop_inner_breaks(self) -> Breaks | None:
        """Gets Breaks instance"""
        try:
            return self._direct_inner_breaks
        except AttributeError:
            self._direct_inner_breaks = cast(Breaks, self._get_style_inst("breaks"))
        return self._direct_inner_breaks

    @property
    def prop_inner_flow_options(self) -> FlowOptions | None:
        """Gets Flow Options instance"""
        try:
            return self._direct_inner_fo
        except AttributeError:
            self._direct_inner_fo = cast(FlowOptions, self._get_style_inst("flow_options"))
        return self._direct_inner_fo

    @static_prop
    def default() -> TextFlow:  # type: ignore[misc]
        """Gets ``TextFlow`` default. Static Property."""
        try:
            return TextFlow._DEFAULT_INST
        except AttributeError:
            hy = Hyphenation.default
            brk = Breaks.default
            flo = FlowOptions.default
            tf = TextFlow()
            tf._set_style("hyphenation", hy, *hy.get_attrs())
            tf._set_style("breaks", brk, *brk.get_attrs())
            tf._set_style("flow_options", flo, *flo.get_attrs())
            tf._is_default_inst = True
            TextFlow._DEFAULT_INST = tf
        return TextFlow._DEFAULT_INST

    # endregion properties