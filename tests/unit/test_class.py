
from temboardagent.errors import UserError
import pgbadger

import pytest


def test_get_pgbadger_reports():

    # empty call
    assert(pgbadger.get_pgbadger_reports(None,None))


def test_get_pgbadger_reports():

    # empty call
    assert(pgbadger.get_pgbadger_reports(None,None))


def test_get_pgbadger_version():

    # empty call
    assert(pgbadger.get_pgbadger_version(None,None))

def test_error():

    assert(pgbadger.error())

def test_class_init():

    from temboardagent.cli import Application, bootstrap

    app = Application()
    p=pgbadger.pgbadgerplugin(app)
    
    assert(p.load())

    assert(p.unload())


