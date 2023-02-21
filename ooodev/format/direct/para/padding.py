"""
Module for managing paragraph padding.

.. versionadded:: 0.9.0
"""
from __future__ import annotations
from typing import Tuple, cast, Type, TypeVar, overload

from ....events.args.cancel_event_args import CancelEventArgs
from ....exceptions import ex as mEx
from ....meta.static_prop import static_prop
from ....utils import props as mProps
from ...kind.format_kind import FormatKind
from ..common.abstract.abstract_padding import AbstractPadding

_TPadding = TypeVar(name="_TPadding", bound="Padding")


class Padding(AbstractPadding):
    """
    Paragraph Padding

    Any properties starting with ``prop_`` set or get current instance values.

    All methods starting with ``fmt_`` can be used to chain together properties.
    """

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
    def from_obj(cls: Type[_TPadding], obj: object) -> _TPadding:
        ...

    @overload
    @classmethod
    def from_obj(cls: Type[_TPadding], obj: object, **kwargs) -> _TPadding:
        ...

    @classmethod
    def from_obj(cls: Type[_TPadding], obj: object, **kwargs) -> _TPadding:
        """
        Gets Padding instance from object

        Args:
            obj (object): UNO object.

        Raises:
            NotSupportedError: If ``obj`` is not supported.

        Returns:
            Padding: Padding that represents ``obj`` padding.
        """
        inst = cls(**kwargs)
        if not inst._is_valid_obj(obj):
            raise mEx.NotSupportedError(f'Object is not supported for conversion to "{cls.__name__}"')

        inst._set(inst._props.left, int(mProps.Props.get(obj, inst._props.left)))
        inst._set(inst._props.right, int(mProps.Props.get(obj, inst._props.right)))
        inst._set(inst._props.top, int(mProps.Props.get(obj, inst._props.top)))
        inst._set(inst._props.bottom, int(mProps.Props.get(obj, inst._props.bottom)))

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

    @static_prop
    def default() -> Padding:  # type: ignore[misc]
        """Gets Padding default. Static Property."""
        try:
            return Padding._DEFAULT_INST
        except AttributeError:
            Padding._DEFAULT_INST = Padding(padding_all=0.35)
            Padding._DEFAULT_INST._is_default_inst = True
        return Padding._DEFAULT_INST

    # endregion properties
