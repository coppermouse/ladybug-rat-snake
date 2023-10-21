# ----------------------------------------
# file: tests/test_box_line_intersect.py
# ----------------------------------------

import pytest
from box_line_intersect import box_line_intersect

@pytest.mark.parametrize( 'args', [
    ( (0,-1,0), (0,1,0), (32,32,32), (1,33) )
])
def test( args ):
    line_start, line_direction, box, expected = args
    assert box_line_intersect( line_start, line_direction, box ) == expected


