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

routes = RouteSet()

@routes.get(b'/pgbadger/version')
def get_pgbadger_version(http_context, app):
    return pgbadger.check_pgbadger_version()

logger = logging.getLogger(__name__) 


#
# load/unload plugin  
#
class pgbadgerPlugin(object):

    def __init__(self, app, **kw):
        self.app = app

    def load(self):
	logger.info('Starting the pgBagder plugin')
	
	try:
	    version=pgbadger.check_pgbadger_version()
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
		
