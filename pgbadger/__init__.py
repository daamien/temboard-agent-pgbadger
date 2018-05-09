##
## Temboard Agent for pgBadger 
##

import logging

from temboardagent.errors import UserError
from temboardagent.routing import RouteSet

from . import pgbadger


logger = logging.getLogger(__name__)

#
# API Version 0
# This API is a Work In Process and highly unstable !
#

routes = RouteSet()

# TODO
# GET  /pgbadger/v0/reports  : list all reports
# GET  /pgbadger/v0/reports/last  : get last report (in json)
# GET  /pgbadger/v0/reports/last/{html,json}  : get last report (in specified format)
# GET  /pgbadger/v0/reports/<timestamp>  : get report by date (in json)
# GET  /pgbadger/v0/reports/<timestamp>/{html,json}  : get report by date (in specified format)
# DEL  /pgbadger/v0/reports/<timestamp> : remove a report by date 

# GET  /pgbadger/v0/reports  : list all reports
@routes.get(b'/pgbadger/v0/reports')
def get_pgbadger_reports(http_context, app):
    try:
        return json.dumps(pgbadger.list_reports())
    except UserError as e:
        return json.dumps(error())

# POST /pgbadger/v0/reports/new  : create a report
@routes.post(b'/pgbadger/v0/reports/new')
def get_pgbadger_reports(http_context, app):
    try:
        return json.dumps(pgbadger.create_report())
    except UserError as e:
        return json.dumps(error())

# GET /pgbadger/v0/version' : show local pgBadger version
@routes.get(b'/pgbadger/v0/version')
def get_pgbadger_version(http_context, app):
    try:
        return json.dumps(pgbadger.check_version())
    except UserError as e:
        return json.dumps(error())


def error():
    response={}
    response['error']='error'
    return response

#
# load/unload plugin  
#
class pgbadgerplugin(object):

    def __init__(self, app, **kw):
        self.app = app

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
        self.app.router.add(routes)

    def unload(self):
        self.app.router.remove(routes)
		
