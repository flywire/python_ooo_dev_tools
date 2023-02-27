from __future__ import annotations

from .....events.args.cancel_event_args import CancelEventArgs
from .....meta.static_prop import static_prop
from ...structs.shadow_struct import ShadowStruct
from ooo.dyn.table.shadow_location import ShadowLocation as ShadowLocation


class Shadow(ShadowStruct):
    def _on_modifing(self, event: CancelEventArgs) -> None:
        if self._is_default_inst:
            raise ValueError("Modifying a default instance is not allowed")
        return super()._on_modifing(event)

    @static_prop
    def empty() -> ShadowStruct:  # type: ignore[misc]
        """Gets empty Shadow. Static Property. when style is applied it remove any shadow."""
        try:
            return Shadow._EMPTY_INST
        except AttributeError:
            Shadow._EMPTY_INST = Shadow(location=ShadowLocation.NONE, transparent=False, color=8421504, width=1.76)
            Shadow._EMPTY_INST._is_default_inst = True
        return Shadow._EMPTY_INST