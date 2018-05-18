##
## Temboard Agent for pgBadger 
##

import logging
import json

from temboardagent.errors import UserError
from temboardagent.routing import RouteSet
from temboardagent.scheduler.taskmanager import WorkerSet
from temboardagent.configuration import OptionSpec
from temboardagent.validators import dir_

from . import pgbadger


logger = logging.getLogger(__name__)

#
# Background tasks
# Generating a report can take a few minutes when processing very large log files
# We're using schedule task to launch report generation
#
workers = WorkerSet()

@workers.register(pool_size=1)

@workers.schedule(id='monprojet_toto', redo_interval=5)
def worker_toto(app):
    logger.info("hello")


#
# API Version 0
# This API is a Work In Process and highly unstable !
#

routes_v0 = RouteSet()

# GET  /pgbadger/v0/reports  : list all reports
@routes_v0.get(b'/pgbadger/v0/reports')
def get_pgbadger_reports(http_context, app):
    try:
        return json.dumps(pgbadger.list_reports(app.config))
    except UserError as e:
        return json.dumps(error())

# GET  /pgbadger/v0/reports/last  : get last report (in json)
@routes_v0.get(b'/pgbadger/v0/reports/last')
def get_pgbadger_report_last(http_context, app):
    try:
        return json.dumps(pgbadger.fetch_last_report(app.config))
    except UserError as e:
        return json.dumps(error())

# GET  /pgbadger/v0/reports/last.html  : get last report (in html)
@routes_v0.get(b'/pgbadger/v0/reports/last.html')
def get_pgbadger_report_last_html(http_context, app):
    try:
        return json.dumps(pgbadger.fetch_last_report_html(app.config))
    except UserError as e:
        return json.dumps(error())

# POST /pgbadger/v0/reports/new  : create a report
@routes_v0.post(b'/pgbadger/v0/reports/new')
def post_pgbadger_reports_new(http_context, app):
    try:
        return json.dumps(pgbadger.create_report(app.config))
    except UserError as e:
        return json.dumps(error())

# GET  /pgbadger/v0/reports/<timestamp>  : get report by date (in json)        
@routes_v0.get(b'/pgbadger/v0/reports/<int:timestamp>')
def get_pgbadger_report_timestamp(http_context, app, timestamp):
    try:
        return json.dumps(pgbadger.fetch_report(app.config,timestamp))
    except UserError as e:
        return json.dumps(error())

# GET  /pgbadger/v0/reports/<timestamp>.html  : get report by date (in html)        
@routes_v0.get(b'/pgbadger/v0/reports/<int:timestamp>.html')
def get_pgbadger_report_timestamp_html(http_context, app, timestamp):
    try:
        return json.dumps(pgbadger.fetch_report_html(app.config,timestamp))
    except UserError as e:
        return json.dumps(error())

# GET /pgbadger/v0/version' : show local pgBadger version
@routes_v0.get(b'/pgbadger/v0/version')
def get_pgbadger_version(http_context, app):
    try:
        return json.dumps(pgbadger.check_version(app.config))
    except UserError as e:
        return json.dumps(error())

# DEL  /pgbadger/v0/reports/<timestamp> : remove a report by date 
@routes_v0.delete(b'/pgbadger/v0/reports/<int:timestamp>')
def delete_pgbadger_report_timestamp(http_context, app,timestamp):
    try:
        return json.dumps(pgbadger.delete_report(app.config,timestamp))
    except UserError as e:
        return json.dumps(error())

def error():
    response={}
    response['error']='error'
    return response


@workers.register(pool_size=1)
def create_report(app):
    return True

#
# load/unload plugin  
#
class pgbadgerplugin(object):

    s = 'pgbadger'
    option_specs = [
        OptionSpec(s, 'pgbadger_path', default=None, validator=dir_),
        OptionSpec(s, 'log_directory', default='/var/log/postgresql', validator=dir_),
        OptionSpec(s, 'reports_directory', default='/var/lib/pgbadger', validator=dir_),
    ]
    del s


    def __init__(self, app, **kw):
        self.app = app
        self.app.config.add_specs(self.option_specs)


    def load(self):
        logger.info('Starting the pgBagder plugin')
	
        try:
            version=pgbadger.check_version()
            logger.info('Found pgBadger version : %s' %version )
        except:
            # if pgBadger is not present, the plugin is useless
            logger.warning('Cannot find pgBadger on the server. The pgBadger plugin will not work properly.')
            logger.info('Check that pgBadger is installed on the server.')
	
        # create API routes
        logger.info('Adding pgBadger routes')
        self.app.router.add(routes_v0)

        self.app.worker_pool.add(workers)
        #self.app.scheduler.add(workers)

    def unload(self):
        #self.app.scheduler.remove(workers)
        self.app.worker_pool.remove(workers)
        self.app.router.remove(routes_v0)
        self.app.config.remove_specs(self.option_specs)

