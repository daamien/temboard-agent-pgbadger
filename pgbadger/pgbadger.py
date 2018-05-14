
import logging
import os
import json
import time
from datetime import datetime,date


from temboardagent.errors import UserError
from temboardagent.command import exec_command

#
# Constants
#

PGBADGER_MIN_VERSION = 6000 # version below 6.0 are not supported
PGBADGER_REPORTS_DIRECTORY = '/var/lib/pgbadger'
POSTGRESQL_LOG_DIRECTORY = '/var/log/postgresql/'

# Python datetime is not Serializable
# we need this handler to convert dates in JSON format
date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, (datetime, date))
    else None
)


logger = logging.getLogger(__name__)


#
# utils
# 

def check_version(config):
    """
    check if the pgBadger version is correct, 
    throws an error is pgBadger is not present or too old
    
    :param path: directory containing the pgBadger binary (optional)
    :return: the version in different formats
    """

    command=['perl', pgbadger_bin(config), '--version']
    (return_code, stdout, stderr) = exec_command(command)

    if return_code!=0:
        msg = "Seems like pgBadger is not installed : %s" %stderr
        raise UserError(msg)

    version=parse_version(stdout)

    if version['int_version'] < PGBADGER_MIN_VERSION:
        msg = "This version of pgBadger is too old : %s" %version['full_version']
        raise UserError(msg)

    return version

def create_report(config):
    """
    TODO
    """
    now=datetime.now()
    metadata={}
    metadata['created_at']=now
    metadata['timestamp']=int(time.mktime(now.timetuple()))

    # output file
    output_args=['--outfile', json_report_filepath(config, metadata['timestamp'])]

    # input file
    try:
    	input_dir = config['log_directory']	or POSTGRESQL_LOG_DIRECTORY
    except:
        msg='Internal Error.'
        raise UserError(msg)
    input_filename='postgresql.log'
    input_args=[os.path.join(input_dir,input_filename)]
    
    # Launch	
    command=['perl', pgbadger_bin(config)] + output_args + input_args
    (return_code, stdout, stderr) = exec_command(command)

    if return_code!=0:
        msg = "pgBadger failed"
        logger.error("%s during command %s with error %s"% (msg,command,stderr))
        raise UserError(msg)

    return metadata	


def fetch_last_report(config):
    """
    Return the last available report
    """
    reports=list_reports(config)
    last=max(reports.keys())
    # copy metadata
    return insert_json(config,reports[last])

def insert_json(config,report):
    # Add the JSON content
    try:
	f= open(json_report_filepath(config,report['timestamp']),'r')
	report['json']=f.read()
    except:
	msg = "Internal Error."
	logger.error("Can't open file : %s" % (msg,command,stderr))
        raise UserError(msg)

    return report	

def fetch_report(config, timestamp):
    """
    """
    reports=list_reports(config)
    return insert_json(config,reports[timestamp])


def list_reports(config):
    """
    TODO
    """
    result={}

    if not 'reports_directory' in config:
        msg = "Internal Error."
        raise UserError(msg)

    target = config['reports_directory'] or PGBADGER_REPORTS_DIRECTORY
    
    try:
        all_files_in_reports_dir=os.listdir(target)
    except:
        msg = "Error while reading the reports directory."
        raise UserError(msg)

    for f in all_files_in_reports_dir:
        if f.endswith(".json"):
            # filename format is supposed to be like that: 
            # 1525794324_pgbadger_report_05may2018.json
            timestamp=int(f.split('_')[0])
            metadata={}
            metadata['timestamp']=timestamp
            metadata['created_at']=datetime.fromtimestamp(timestamp)
            metadata['url_json']='/pgbadger/v0/reports/%d/json' % timestamp
            metadata['url_html']='/pgbadger/v0/reports/%d/html' % timestamp
            result[timestamp]=metadata

    return result

#
# utils
#


def json_report_filepath(config,timestamp):
    """
    """	 
    # filename format is supposed to be like that: 
    # 1525794324_pgbadger_report_05may2018.json
    created_at=datetime.fromtimestamp(timestamp).strftime('%d%b%Y')
    report_filename=str(timestamp)+'_pgbadger_report_'+created_at+'.json'
    return os.path.join(reports_directory(config),report_filename)

def pgbadger_bin(config):
    try:
	return os.path.join( config['pgbadger_path'] or '' , 'pgbadger' )
    except:
        msg='Internal Error.'
        raise UserError(msg)


def reports_directory(config):
    try:
	return config['reports_directory'] or PGBADGER_REPORTS_DIRECTORY
    except:
	msg='Internal Error.'
	raise UserError(msg)	

def parse_version(version):
    """
    Extract pgBadger version from string
    
    :param version: a full version string, usually provided by `pgbadger --version`
    :return: the version number in different formats
    """
    result={}
    # example with version = "pgBadger Version 3.4\n"
    
    # full_version = "pgBadger Version 3.4"
    result['full_version']=version.strip()
    
    # short_version = "3.4"
    result['short_version']=result['full_version'].split(' ')[2]
    
    # int_version = 3004
    spl=result['short_version'].split('.')
    major,minor=spl[0],spl[1]
    result['int_version']=int(major+minor.zfill(3))

    return result
