from __future__ import annotations
import pytest
if __name__ == "__main__":
    pytest.main([__file__])
from ooodev.utils.gui import GUI
from ooodev.utils.lo import Lo
from ooodev.utils.props import Props
from ooodev.office.calc import Calc
from com.sun.star.sheet import XSpreadsheet




def test_build_cells(loader) -> None:
    doc = Calc.create_doc(loader=loader)
    assert doc is not None, "Could not open create new document"
    visible = False
    delay = 0
    if visible:
        GUI.set_visible(is_visible=visible, odoc=doc)
    sheet = Calc.get_sheet(doc=doc, index=0)

    header_vals = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    for i, val in enumerate(header_vals):
        Calc.set_val(sheet=sheet, column=i, row=0, value=val)

    vals = (31.45, 20.9, 117.5, 23.4, 114.5, 115.3, 171.3, 89.5, 41.2, 71.3, 25.4, 38.5)

    for i, val in enumerate(vals):
        Calc.set_val(sheet=sheet, column=i, row=1, value=val)
    
    for i, val in enumerate(header_vals):
        assert val == Calc.get_string(sheet=sheet, column=i, row=0)
    
    for i, val in enumerate(vals):
        assert val == pytest.approx(Calc.get_num(sheet=sheet, column=i, row=1), rel=1e-4)

    Lo.delay(delay)
    Lo.close(closeable=doc, deliver_ownership=False)


def test_build_rows(loader) -> None:
    doc = Calc.create_doc(loader=loader)
    assert doc is not None, "Could not open create new document"
    visible = False
    delay = 0
    if visible:
        GUI.set_visible(is_visible=visible, odoc=doc)
    sheet = Calc.get_sheet(doc=doc, index=0)

    vals = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    col = 1
    row = 0
    cell_name = Calc.get_cell_str(col=col, row=row)
    Calc.set_row(
        sheet=sheet,
        cell_name=cell_name,
        values=vals
    )
    cell_range = Calc.get_cell_range(
        sheet=sheet,
        start_col=col,
        start_row=row,
        end_col= col + (len(vals) - 1),
        end_row=row
    )
    sheet_vals = Calc.get_array(cell_range=cell_range)
    assert sheet_vals is not None, 'Unable to get values from sheet'
    for i, val in enumerate(sheet_vals[0]):
        assert val == vals[i]
        
    
    vals = (42, 58.9, -66.5, 43.4, 44.5, 45.3, -67.3, 30.5, 23.2, -97.3, 22.4, 23.5)
    col = 1
    row = 1
    cell_name = Calc.get_cell_str(col=col, row=row)
    cell_range = Calc.get_cell_range(
        sheet=sheet,
        start_col=col,
        start_row=row,
        end_col= col + (len(vals) - 1),
        end_row=row
    )

    Calc.set_val(sheet=sheet, cell_name="N1", value="SUM")
    Calc.set_val(sheet=sheet, cell_name="A2", value="Smith")

    Calc.set_row(sheet=sheet, cell_name=cell_name, values=vals)
    Calc.set_val(sheet=sheet, cell_name="N2", value="=SUM(B2:M2)")
    Calc.set_val(sheet=sheet, column=0, row=2, value="Jones")
    
    sheet_vals = Calc.get_array(cell_range=cell_range)
    assert sheet_vals is not None, 'Unable to get values from sheet'
    for i, val in enumerate(sheet_vals[0]):
        assert vals[i] ==  pytest.approx(val, rel=1e-4)

    
    Lo.delay(delay)
    vals = (21, 40.9, -57.5, -23.4, 34.5, 59.3, 27.3, -38.5, 43.2, 57.3, 25.4, 28.5)
    col = 1
    row = 2
    cell_name = Calc.get_cell_str(col=col, row=row)
    cell_range = Calc.get_cell_range(
        sheet=sheet,
        start_col=col,
        start_row=row,
        end_col= col + (len(vals) - 1),
        end_row=row
    )

    Calc.set_row(
        sheet=sheet,
        col_start=col,
        row_start=row,
        values=vals
    )
    Calc.set_val(sheet=sheet, column=13, row=2, value="=SUM(B3:M3)")
    Calc.set_val(sheet=sheet, column=0, row=3, value="Brown")
    sheet_vals = Calc.get_array(cell_range=cell_range)
    assert sheet_vals is not None, 'Unable to get values from sheet'
    for i, val in enumerate(sheet_vals[0]):
        assert vals[i] ==  pytest.approx(val, rel=1e-4)
        


    vals = (31.45, -20.9, -117.5, 23.4, -114.5, 115.3, -171.3, 89.5, 41.2, 71.3, 25.4, 38.5)
    col = 1
    row = 3
    cell_name = Calc.get_cell_str(col=col, row=row)
    cell_range = Calc.get_cell_range(
        sheet=sheet,
        start_col=col,
        start_row=row,
        end_col= col + (len(vals) - 1),
        end_row=row
    )
    Calc.set_row(
        sheet=sheet,
        col_start=col,
        row_start=row,
        values=vals
    )
    Calc.set_val(sheet=sheet, column=13, row=3, value="=SUM(A4:L4)")
    sheet_vals = Calc.get_array(cell_range=cell_range)
    assert sheet_vals is not None, 'Unable to get values from sheet'
    for i, val in enumerate(sheet_vals[0]):
        assert vals[i] ==  pytest.approx(val, rel=1e-4)

    Lo.delay(delay)
    Lo.close(closeable=doc, deliver_ownership=False)


def build_cols(sheet: XSpreadsheet) -> None:
    Calc.set_col(
        sheet=sheet,
        cell_name="A2",
        values=("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"),
    )
    Calc.set_val(sheet=sheet, cell_name="A14", value="SUM")
    Calc.set_val(sheet=sheet, cell_name="B1", value="Smith")
    Calc.set_col(
        sheet=sheet, cell_name="B2", values=(42, 58.9, -66.5, 43.4, 44.5, 45.3, -67.3, 30.5, 23.2, -97.3, 22.4, 23.5)
    )
    Calc.set_val(sheet=sheet, cell_name="B14", value="=SUM(B2:M2)")
    Calc.set_val(sheet=sheet, column=2, row=0, value="Jones")
    Calc.set_col(
        sheet=sheet,
        col_start=2,
        row_start=1,
        values=(21, 40.9, -57.5, -23.4, 34.5, 59.3, 27.3, -38.5, 43.2, 57.3, 25.4, 28.5),
    )
    Calc.set_val(sheet=sheet, column=2, row=13, value="=SUM(B3:M3)")
    Calc.set_val(sheet=sheet, column=3, row=0, value="Brown")
    Calc.set_col(
        sheet=sheet,
        col_start=3,
        row_start=1,
        values=(31.45, -20.9, -117.5, 23.4, -114.5, 115.3, -171.3, 89.5, 41.2, 71.3, 25.4, 38.5),
    )
    Calc.set_val(sheet=sheet, column=3, row=13, value="=SUM(A4:L4)")


def build_array(sheet: XSpreadsheet) -> None:
    vals = (
        ("", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"),
        ("Smith", 42, 58.9, -66.5, 43.4, 44.5, 45.3, -67.3, 30.5, 23.2, -97.3, 22.4, 23.5),
        ("Jones", 21, 40.9, -57.5, -23.4, 34.5, 59.3, 27.3, -38.5, 43.2, 57.3, 25.4, 28.5),
        ("Brown", 31.45, -20.9, -117.5, 23.4, -114.5, 115.3, -171.3, 89.5, 41.2, 71.3, 25.4, 38.5),
    )
    Calc.set_array(values=vals, sheet=sheet, name="A1:M4")  # or just A1

    Calc.set_val(sheet=sheet, cel_name="N1", value="SUM")
    Calc.set_val(sheet=sheet, cel_name="N2", value="=SUM(B2:M2)")
    Calc.set_val(sheet=sheet, cel_name="N3", value="=SUM(B3:M3)")
    Calc.set_val(sheet=sheet, cel_name="N4", value="=SUM(A4:L4)")


def convert_addresses(sheet: XSpreadsheet) -> None:
    pos = Calc.get_cell_position(cell_name="AA2")
    print(f"Position of AA2: ({pos.X}, {pos.Y})")

    cell = Calc.get_cell(sheet=sheet, column=pos.X, row=pos.Y)
    Calc.print_cell_address(cell=cell)

    print(f"AA2: {Calc.get_cell_str(col=pos.X, row=pos.Y)}")
    print()

    rng = Calc.get_cell_range_positions(range_name="A1:D5")
    rf = rng[0]
    rs = rng[1]
    print(f"Range of A1:D5: ({rf.X}, {rf.Y}) -- ({rs.Y}, {rs.X})")
    cell_range = Calc.get_cell_range(sheet=sheet, start_col=rf.X, start_row=rf.Y, end_col=rs.X, end_row=rs.Y)
    Calc.print_address(cell_range=cell_range)
    print(f"A1:D5: {Calc.get_range_str(rf.X, rf.Y, rs.X, rs.Y)}")
    print()
