# Author: Richard Belleville

import pytest
from ..environment.environment import *

def test_example7(capsys):
    # tests the return statement
    env = Environment(file="../../examples/example7.prog")
    env.evaluate()
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "4\n2\n"
