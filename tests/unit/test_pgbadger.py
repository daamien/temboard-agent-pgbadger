
from pgbadger import pgbadger

import pytest

def test_parse_version():
    
    test1="pgBadger Version 3.4\n"
    assert(pgbadger.parse_version(test1))
    
    v=pgbadger.parse_version(test1)
    assert(v['int_version'] == 3004)

