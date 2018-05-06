
import os

from temboardagent.errors import UserError
from temboardagent.command import exec_command


def check_pgbadger_version():
    """
    returns the pgBadger version, throws an error is pgBadger is not present 
    """
    command=['pgbadger', '--version']
    (return_code, stdout, stderr) = exec_command(command)

    if return_code!=0:
        msg = "Seems like pgBadger is not installed : %s" %stderr
        raise UserError(msg)
    
    return "{ 'version' : '%s' }" %stdout
