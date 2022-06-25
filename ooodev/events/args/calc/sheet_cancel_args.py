# coding: utf-8
from __future__ import annotations
from typing import Any
from .sheet_args import SheetArgs
from ..cancel_event_args import CancelEventArgs

class SheetCancelArgs(CancelEventArgs, SheetArgs):
    """
    Sheet Cancel Event Args
    """
    def __init__(self, source: Any, cancel=False) -> None:
        """
        Constructor

        Args:
            source (Any): Event Source
            cancel (bool, optional): Cancel value. Defaults to False.
        """
        super().__init__(source=source, cancel=cancel)        
