
import os
import json

from temboardagent.errors import UserError
from temboardagent.command import exec_command

#
# Constants
#


MIN_PGBADGER_VERSION = 6000 # version below 6.0 are not supported

#
# API entrpoints
#
def get_version():
    try:
        response=check_pgbadger_version()
    except UserError as ue:
        response={}
        response['error']=ue
    return json.dumps(response)

#
#
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

    if version['int_version'] < MIN_PGBADGER_VERSION:
        msg = "This version of pgBadger is too old : %s" %version['full_version']
        raise UserError(msg)

    return version


def parse_version(version):
    """
    Extract version from string
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
