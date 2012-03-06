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

import logging
class RaceController(webapp.RequestHandler):
  
  def __init__(self):
        self.raceService = RaceService()
        
  def get(self, raceKey):
    
    if not users.get_current_user():
        """ If users are not logged in redirect to a login page """
        url = users.create_login_url(self.request.uri)
        self.redirect(url, False)
        return;
    
    race = Race.get(raceKey)
    
    my_runner = self.raceService.joinRace(users.get_current_user(), race)
    
    channel_token = channel.create_channel(str(my_runner.key()))
    
    template_values = {
      'race_name': race.name,
      'race_key': raceKey,
      'race_description': race.description,
      'race_status': race.status,
      'runner_key': str(my_runner.key()),
      'runner_ready' : "true" if my_runner.ready else "false",
      'channel_token': channel_token,
      'runners' : self.raceService.getRunnersAsModel(race)
    }
    
    
    logging.error(my_runner.ready);
    
    path = os.path.join(os.path.dirname(__file__), '../../templates/show-race.html')
    self.response.out.write(template.render(path, template_values))
    
    self.raceService.sendUpdateToRunners(my_runner, race)
      
  def post(self):
    race = Race()

    if users.get_current_user():
      race.admin = users.get_current_user()

    race.name = self.request.get('name')
    race.description = self.request.get('description')
    race.status = "lobby"
    
    race.put()
    self.redirect('/race/' + str(race.key()))
    


class RacePodiumRequestHandler(webapp.RequestHandler):
  
  def __init__(self):
        self.raceService = RaceService()
        
  def get(self, raceKey):
    """ Render a html portion showing the race podium """
    race = Race.get(raceKey)
    
    self.raceService.getRunnersAsModel(race)
    
    template_values = {
      'runners' : self.raceService.getRunnersAsModel(race)
    }
    
    path = os.path.join(os.path.dirname(__file__), '../../templates/show-race-podium.html')
    self.response.out.write(template.render(path, template_values))

    
