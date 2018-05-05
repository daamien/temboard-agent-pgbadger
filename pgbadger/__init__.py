##
## Temboard Agent for pgBadger 
##

import logging

from temboardagent.errors import UserError
from temboardagent.routing import RouteSet

from . import pgbadger

#
# API Entrypoints
#

@routes.get(b'/pgbadger/version')
def get_pgbadger_version(http_context, app):
    return pgbadger.check_pgbadger_version(conn)

logger = logging.getLogger(__name__) 

routes = RouteSet()

#
# 
#
class PgbadgerPlugin(object):

    def __init__(self, app, **kw):
        self.app = app

    def load(self):
	logger.info('Starting the pgBagder plugin')
	
	# if pgBadger is not present, the plugin is useless
	try:
	    pgbadger.check_pgbadger_version()
	except:
	    logger.warning('Cannot find pgBadger on the server. The pgBadger will not work properly.')
	    logger.info('Check that pgBadger is installed on the server.')
	
	# create API routes
        self.app.router.add(routes)

    def unload(self):
        self.app.router.remove(routes)
		
