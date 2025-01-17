from __future__ import annotations
from dataclasses import dataclass
from typing import overload
from . import range_obj as mRngObj
from .. import table_helper as mTb
from ...office import calc as mCalc
from ..decorator import enforce

import uno
from ooo.dyn.table.cell_range_address import CellRangeAddress


@enforce.enforce_types
@dataclass(frozen=True)
class RangeValues:
    """
    Range Parts. Intended to be zero-based indexes

    .. versionadded:: 0.8.2
    """

    col_start: int
    """Column start such as ``0``"""
    col_end: int
    """Column end such as ``3``"""
    row_start: int
    """Row start such as ``0``"""
    row_end: int
    """Row end such as ``125``"""
    sheet_idx: int = -1
    """Sheet index that this range value belongs to"""

    def __post_init__(self):
        if self.sheet_idx < 0:
            try:
                idx = mCalc.Calc.get_sheet_index()
                object.__setattr__(self, "sheet_idx", idx)
            except:
                pass

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeValues):
            return (
                self.col_start == other.col_start
                and self.col_end == other.col_end
                and self.row_start == other.row_start
                and self.row_end == other.row_end
                and self.sheet_idx == other.sheet_idx
            )
        if isinstance(other, mRngObj.RangeObj):
            return str(self) == str(other)
        if isinstance(other, str):
            return str(self) == other.upper()
        return False

    def __str__(self) -> str:
        start = mTb.TableHelper.make_cell_name(row=self.row_start, col=self.col_start, zero_index=True)
        end = mTb.TableHelper.make_cell_name(row=self.row_end, col=self.col_end, zero_index=True)
        return f"{start}:{end}"

    # region from_range()
    @overload
    @staticmethod
    def from_range(range_val: CellRangeAddress) -> RangeValues:
        ...

    @overload
    @staticmethod
    def from_range(range_val: mRngObj.RangeObj) -> RangeValues:
        ...

    @overload
    @staticmethod
    def from_range(range_val: str) -> RangeValues:
        ...

    @staticmethod
    def from_range(range_val: str | mRngObj.RangeObj | CellRangeAddress) -> RangeValues:
        """
        Gets a ``RangeValues`` instance from a range

        Args:
            range (str | mRngObj.RangeObj | CellRangeAddress): Range as object or string (``A2:G23``).

        Returns:
            RangeValues: Object representing range values.
        """
        if isinstance(range_val, mRngObj.RangeObj):
            col_start = mTb.TableHelper.col_name_to_int(range_val.col_start, True)
            col_end = mTb.TableHelper.col_name_to_int(range_val.col_end, True)
            row_start = range_val.row_start - 1
            row_end = range_val.row_end - 1
            sheet_idx = range_val.sheet_idx
        elif isinstance(range_val, str):
            parts = mTb.TableHelper.get_range_parts(range_val)
            col_start = mTb.TableHelper.col_name_to_int(parts.col_start, True)
            col_end = mTb.TableHelper.col_name_to_int(parts.col_end, True)
            row_start = parts.row_start - 1
            row_end = parts.row_end - 1
            sheet_name = parts.sheet
            sheet_idx = -1
            if sheet_name:
                sheet = mCalc.Calc.get_sheet(doc=mCalc.Calc.open_doc(), sheet_name=sheet_name)
                sheet_idx = mCalc.Calc.get_sheet_index(sheet)
        else:
            # CellRange
            col_start = range_val.StartColumn
            col_end = range_val.EndColumn
            row_start = range_val.StartRow
            row_end = range_val.EndRow
            sheet_idx = range_val.Sheet

        return RangeValues(
            col_start=col_start, row_start=row_start, col_end=col_end, row_end=row_end, sheet_idx=sheet_idx
        )

    # endregion from_range()

    def get_range_obj(self) -> mRngObj.RangeObj:
        """
        Gets a ``RangeObj``

        Returns:
            RangeObj: Range object.
        """
        return mRngObj.RangeObj.from_range(self)

    def get_cell_range_address(self) -> CellRangeAddress:
        """
        Gets a Cell Range Address

        Returns:
            CellRangeAddress: Cell range Address
        """
        return CellRangeAddress(
            Sheet=self.sheet_idx,
            StartColumn=self.col_start,
            StartRow=self.row_start,
            EndColumn=self.col_end,
            EndRow=self.row_end,
        )

    def is_single_col(self) -> bool:
        """
        Gets if instance is a single column or multi-column

        Returns:
            bool: ``True`` if single column; Otherwise, ``False``

        Note:
            If instance is a single cell address then ``True`` is returned.
        """
        return self.col_start == self.col_end

    def is_single_row(self) -> bool:
        """
        Gets if instance is a single row or multi-row

        Returns:
            bool: ``True`` if single row; Otherwise, ``False``

        Note:
            If instance is a single cell address then ``True`` is returned.
        """
        return self.row_start == self.row_end

    def is_single_cell(self) -> bool:
        """
        Gets if a instance is a single cell or a range

        Returns:
            bool: ``True`` if single cell; Otherwise, ``False``
        """
        return self.is_single_col() and self.is_single_row()
