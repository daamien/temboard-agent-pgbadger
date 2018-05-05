
import os

from temboardagent.errors import UserError

def check_pgbadger_version():
    pgbadger_version='x'
    if not pgbadger_version:
        msg = "Seems like pgBadger is not installed."
        raise UserError(msg)
