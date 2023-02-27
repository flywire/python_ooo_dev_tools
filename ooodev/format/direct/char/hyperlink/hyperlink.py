"""
Module for creating hyperlinks

.. versionadded:: 0.9.0
"""
# region imports
from __future__ import annotations
from typing import Tuple, overload, Type, TypeVar
from enum import Enum

from .....events.args.cancel_event_args import CancelEventArgs
from .....exceptions import ex as mEx
from .....meta.static_prop import static_prop
from .....utils import lo as mLo
from .....utils import props as mProps
from ....kind.format_kind import FormatKind
from ....style_base import StyleBase
from ...common.props.hyperlink_props import HyperlinkProps
from ...frame.hyperlink.link_to import LinkTo, TargetKind as TargetKind


# endregion imports

_THyperlink = TypeVar(name="_THyperlink", bound="Hyperlink")


class Hyperlink(LinkTo):
    """
    Hyperlink

    .. versionadded:: 0.9.0
    """

    # region init

    def __init__(
        self,
        *,
        name: str | None = None,
        url: str | None = None,
        target: TargetKind | str = TargetKind.NONE,
        visited_style: str = "Visited Internet Link",
        unvisited_style: str = "Internet link",
    ) -> None:
        """
        Constructor

        Args:
            name (str, optional): Link name.
            url (str, optional): Link Url.
            target (TargetKind, str, optional): Link target. Defaults to ``TargetKind.NONE``.
            visited_style (str, optional): Link visited style. Defaults to ``Internet link``.
            unvisited_style (str, optional): Link unvisited style. Defaults to ``Visited Internet Link``.

        Returns:
            None:
        """

        super().__init__(name=name, url=url, target=target)
        self.prop_visited_style = visited_style
        self.prop_unvisited_style = unvisited_style

    # endregion init

    # region methods
    def _supported_services(self) -> Tuple[str, ...]:
        try:
            return self._supported_services_values
        except AttributeError:
            self._supported_services_values = (
                "com.sun.star.style.CharacterProperties",
                "com.sun.star.style.CharacterStyle",
            )
        return self._supported_services_values

    # region from_obj()
    @overload
    @classmethod
    def from_obj(cls: Type[_THyperlink], obj: object) -> _THyperlink:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_THyperlink], obj: object, **kwargs) -> _THyperlink:
        ...

    @classmethod
    def from_obj(cls: Type[_THyperlink], obj: object, **kwargs) -> _THyperlink:
        """
        Gets hyperlink instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            Hyperlink: Hyperlink that represents ``obj`` Hyperlink.
        """
        inst = cls(**kwargs)
        if not inst._is_valid_obj(obj):
            raise mEx.NotSupportedError(f'Object is not supported for conversion to "{cls.__name__}"')

        inst._set(inst._props.name, mProps.Props.get(obj, inst._props.name))
        inst._set(inst._props.url, mProps.Props.get(obj, inst._props.url))
        inst._set(inst._props.target, mProps.Props.get(obj, inst._props.target))
        inst._set(inst._props.visited, mProps.Props.get(obj, inst._props.visited))
        inst._set(inst._props.unvisited, mProps.Props.get(obj, inst._props.unvisited))

        return inst

    # endregion from_obj()
    # endregion methods

    # region Properties
    @property
    def prop_visited_style(self) -> str:
        """Gets/Sets visited style"""
        return self._get(self._props.visited)

    @prop_visited_style.setter
    def prop_visited_style(self, value: str):
        self._set(self._props.visited, value)

    @property
    def prop_unvisited_style(self) -> str:
        """Gets/Sets style for links that have not yet been visited"""
        return self._get(self._props.unvisited)

    @prop_unvisited_style.setter
    def prop_unvisited_style(self, value: str):
        self._set(self._props.unvisited, value)

    @property
    def prop_format_kind(self) -> FormatKind:
        """Gets the kind of style"""
        try:
            return self._format_kind_prop
        except AttributeError:
            self._format_kind_prop = FormatKind.CHAR
        return self._format_kind_prop

    @property
    def _props(self) -> HyperlinkProps:
        try:
            return self._props_internal_attributes
        except AttributeError:
            self._props_internal_attributes = HyperlinkProps(
                name="HyperLinkName",
                target="HyperLinkTarget",
                url="HyperLinkURL",
                visited="VisitedCharStyleName",
                unvisited="UnvisitedCharStyleName",
            )
        return self._props_internal_attributes

    @static_prop
    def empty() -> Hyperlink:  # type: ignore[misc]
        """Gets Highlight empty. Static Property."""
        try:
            return Hyperlink._EMPTY_INST
        except AttributeError:
            Hyperlink._EMPTY_INST = Hyperlink(name="", url="")
            Hyperlink._EMPTY_INST._is_default_inst = True
        return Hyperlink._EMPTY_INST

    # endregion Properties