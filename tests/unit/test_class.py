
from temboardagent.errors import UserError
import pgbadger

import pytest


def test_get_pgbadger_reports():

    # empty call
    assert(pgbadger.get_pgbadger_reports(None,None))


def test_post_pgbadger_reports_new():

    # empty call
    assert(pgbadger.post_pgbadger_reports_new(None,None))


def test_get_pgbadger_version():

    # empty call
    assert(pgbadger.get_pgbadger_version(None,None))

def test_error():

    assert(pgbadger.error())

def test_class_init():

    from temboardagent.cli import Application
    from temboardagent.routing import Router
    app = Application()
    app.router = Router()
 
    p=pgbadger.pgbadgerplugin(app)
    
    assert(p.load() is None)

    assert(p.unload() is None)


