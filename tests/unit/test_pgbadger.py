
from temboardagent.errors import UserError
from pgbadger import pgbadger

import json
import pytest

empty_config={}

injection_config={}
injection_config['reports_directory']='_tmp/reports; echo "injection"'
injection_config['log_directory']='_tmp/log; echo "injection"'
injection_config['pgbadger_path']='; echo "injection"' 

test_config={}
test_config['reports_directory']='_tmp/reports'
test_config['log_directory']='_tmp/log'
test_config['pgbadger_path']='src/pgBadger/'

def test_parse_version():
    
    test1="pgBadger Version 3.4\n"
    assert(pgbadger.parse_version(test1))
    
    v=pgbadger.parse_version(test1)
    assert(v['int_version'] == 3004)

def test_check_version():
    
    version_config={}

    # latest
    version_config['pgbadger_path']='src/pgBadger/'
    assert(pgbadger.check_version(version_config))
    
    # old but ok
    version_config['pgbadger_path']='src/pgBadger-9.0/'
    assert(pgbadger.check_version(version_config))

    # too old
    version_config['pgbadger_path']='src/pgBadger-3.3/'
    with pytest.raises(UserError):
        assert(pgbadger.check_version(version_config))

    # non exitent path
    version_config['pgbadger_path']='/cnjcnvnsjdvnkdnvkdjvnksndvs/'
    with pytest.raises(UserError):
        assert(pgbadger.check_version(version_config))

    # not installed 
    with pytest.raises(UserError):
        assert(pgbadger.check_version(empty_config))

def test_create_report():

    # should not work on a test environment
    with pytest.raises(UserError):
        assert(pgbadger.create_report(empty_config))	

    # 
    test_config_no_logs={}
    test_config_no_logs['reports_directory']='_tmp/reports'	
    with pytest.raises(UserError):
	assert(pgbadger.create_report(test_config_no_logs))	

    assert(pgbadger.create_report(test_config))

    # let's try some basic shell injection
    with pytest.raises(UserError):
        assert(pgbadger.create_report(injection_config))


def test_delete_report():

    # Bad config + Bad Timestamp 
    with pytest.raises(UserError):
        assert(pgbadger.delete_report(empty_config,0))

    # Good Config + Bad Timestamp
    with pytest.raises(UserError):
        assert(pgbadger.delete_report(test_config,0))

    # Good Config + Good Timestamp
    response=pgbadger.delete_report(test_config,1525806347)
    assert(response['result']=='Report Removed Succesfully')


def test_fetch_report():
    # Bad config + Bad Timestamp 
    with pytest.raises(UserError):
        assert(pgbadger.fetch_report(empty_config,0))

    # Good Config + Bad Timestamp
    with pytest.raises(UserError):
        assert(pgbadger.fetch_report(test_config,0))

    # Good Config + Good Timestamp
    response=pgbadger.fetch_report(test_config,1526304086)
    assert(response['timestamp']==1526304086)
    assert('user_info' in response['json'])


def test_fetch_report_html():
    # Bad config + Bad Timestamp 
    with pytest.raises(UserError):
        assert(pgbadger.fetch_report_html(empty_config,0))

    # Good Config + Bad Timestamp
    with pytest.raises(UserError):
        assert(pgbadger.fetch_report_html(test_config,0))

    # Good Config + Good Timestamp
    response=pgbadger.fetch_report_html(test_config,1526304086)
    assert('<html>' in response)

def test_fetch_last_report():

    # should not work
    with pytest.raises(UserError):
        assert(pgbadger.fetch_last_report({}))

    config={}
    config['reports_directory']='_tmp/reports'
    
    report=pgbadger.fetch_last_report(config)
    report_json=json.loads(report["json"])
    assert('user_info' in report_json)
    #print(report)


def test_fetch_last_report_html():

    # Bad config 
    with pytest.raises(UserError):
        assert(pgbadger.fetch_last_report_html(empty_config))

    # Good config
    report=pgbadger.fetch_last_report_html(test_config)
    assert('<html lang="en">' in report)
    #print(report)


def test_list_reports():

    # should not work on a test environment
    with pytest.raises(UserError):
        assert(pgbadger.list_reports({}))

    config={}
    config['reports_directory']='/vnsfvnskjdnvskdnvksvn'
    with pytest.raises(UserError):
        pgbadger.list_reports(config)
    
    config={}
    config['reports_directory']='_tmp/reports'
    assert(pgbadger.list_reports(config))


def test_parse_version():

    test1="pgBadger Version 3.4\n"
    assert(pgbadger.parse_version(test1))

    v=pgbadger.parse_version(test1)
    assert(v['int_version'] == 3004)
