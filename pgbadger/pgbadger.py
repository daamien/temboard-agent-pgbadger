
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

def check_version(path=None):
    """
    check if the pgBadger version is correct, 
    throws an error is pgBadger is not present or too old
    
    :param path: directory containing the pgBadger binary (optional)
    :return: the version in different formats
    """
    pgbadger_bin=os.path.join( path or '' , 'pgbadger' )
    command=['perl', pgbadger_bin, '--version']
    
    (return_code, stdout, stderr) = exec_command(command)

    if return_code!=0:
        msg = "Seems like pgBadger is not installed : %s" %stderr
        raise UserError(msg)

    version=parse_version(stdout)

    if version['int_version'] < PGBADGER_MIN_VERSION:
        msg = "This version of pgBadger is too old : %s" %version['full_version']
        raise UserError(msg)

    return version

def create_report(path=None,reports_dir=None,log_dir=None):
    """
    TODO
    """
    now=datetime.now()
    metadata={}
    metadata['created_at']=now
    metadata['timestamp']=int(time.mktime(now.timetuple()))

    pgbadger_bin=os.path.join( path or '' , 'pgbadger' )

    output_dir= reports_dir or PGBADGER_REPORTS_DIRECTORY
    output_filename=str(metadata['timestamp'])+'_pgbadger_report_'+metadata['created_at'].strftime('%d%b%Y')+'.json' 
    output_args=['--outfile', os.path.join(output_dir,output_filename)]

    input_dir = log_dir	or POSTGRESQL_LOG_DIRECTORY
    input_filename='postgresql.log'
    input_args=[os.path.join(input_dir,input_filename)]
    	
    command=['perl', pgbadger_bin] + output_args + input_args

    (return_code, stdout, stderr) = exec_command(command)

    if return_code!=0:
        msg = "pgBadger failed"
        logger.error("%s during command %s with error %s"% (msg,command,stderr))
        raise UserError(msg)

    return metadata	

def list_reports(reports_dir=None):
    """
    TODO
    """
    result={}
    target = reports_dir or PGBADGER_REPORTS_DIRECTORY
    
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
