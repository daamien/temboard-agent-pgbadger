
from temboardagent.errors import UserError
from pgbadger import pgbadger

import pytest

def test_parse_version():
    
    test1="pgBadger Version 3.4\n"
    assert(pgbadger.parse_version(test1))
    
    v=pgbadger.parse_version(test1)
    assert(v['int_version'] == 3004)

def test_check_version():
    
    # latest
    assert(pgbadger.check_version('src/pgBadger/'))
    
    # old but ok
    assert(pgbadger.check_version('src/pgBadger-9.0/'))

    # too old
    with pytest.raises(UserError):
        assert(pgbadger.check_version('src/pgBadger-3.3/'))

    # not installed 
    with pytest.raises(UserError):
        assert(pgbadger.check_version())

def test_create_report():

    # should not work on a test environment
    with pytest.raises(UserError):
        assert(pgbadger.create_report())	

    assert(pgbadger.create_report(
                path='src/pgBadger/',
                reports_dir='_tmp/reports',
                log_dir='_tmp/log')
    )

def test_list_reports():

    # should not work on a test environment
    with pytest.raises(UserError):
        assert(pgbadger.list_reports())

    assert(pgbadger.list_reports(reports_dir='_tmp/reports'))



def test_parse_version():

    test1="pgBadger Version 3.4\n"
    assert(pgbadger.parse_version(test1))

    v=pgbadger.parse_version(test1)
    assert(v['int_version'] == 3004)
