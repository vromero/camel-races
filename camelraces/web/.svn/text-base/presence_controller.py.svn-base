#
# This file is part of CamelRaces 
#
# Copyright(c) 2011 Victor Romero.
# http://www.calamidad.org
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import channel

from camelraces.model.race import Race
from camelraces.model.runner import Runner
from camelraces.service.race_service import RaceService

class DisconnectedController(webapp.RequestHandler):
  
  def __init__(self):
        self.raceService = RaceService()
        
  def post(self):
    runner_key = self.request.get('from')
    
    runner = Runner.get(runner_key)
    race = runner.race
    
    self.raceService.sendDisconnectedToRunners(runner, race)
    runner.delete()
    
    # TODO race may need to be started here if everyone is ready
