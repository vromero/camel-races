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

from google.appengine.ext import db

from camelraces.model.runner import Runner
from camelraces.model.race import Race
from google.appengine.api import channel
from django.utils import simplejson

import logging


class RaceService:
    
  def getRunnerForUser(self, race, user):
      race_runners = Runner.gql("WHERE user = :1 and race = :2", user, race)

  def areAllRunnersReady(self, race):
      total_runners = race.runner_set.count();
      ready_runners = Runner.gql("WHERE race = :1 and ready = true", race).count()
      
      logging.error(total_runners)
      logging.error(ready_runners)
      
      return total_runners == ready_runners

  def sendToRunners(self, race, message):
      runners = race.runner_set
    
      for runner in runners:
        channel.send_message(str(runner.key()), message)
        
  def startRace(self, race):
     self.setRaceStatus(race, "started"); 
     self.sendToRunners(race, '{"messageType" : "start"}');
     
  def setRaceStatus(self, race, status):
      race.status = status;
      race.put();
      
  def getRunnersAsModel(self, race, visible=True):
      ret = []
      runners = race.runner_set.order('-position')
      
      for runner in runners:
          ret.append({
                'runner_key': str(runner.key()),
                'runner_name': runner.user.nickname(), 
                'runner_position': runner.position,
                'runner_visible' : visible,
                'runner_ready' : runner.ready
          });

      return ret;

  def joinRace(self, user, race):
      runners = race.runner_set
        
      race_runners = Runner.gql("WHERE user = :1 and race = :2", user, race)
    
      if (race_runners.count() == 0):
          my_runner = Runner(user=user, race=race, position=0, ready=False);
          my_runner.put()
      else :
          my_runner = race_runners[0]
      logging.error(my_runner.to_xml())
      return my_runner

  def sendUpdateToRunners(self, runner, race):
     runnerUpdateModel = {"messageType" : "gameUpdate", "payload" : { str(runner.key()) : runner.position }}
     self.sendToRunners(runner.race, simplejson.dumps(runnerUpdateModel))

  def sendDisconnectedToRunners(self, runner, race):
     runnerDisconnectedModel = {"messageType" : "runnerDisconnected", "payload" : { str(runner.key()) : runner.position }}
     self.sendToRunners(runner.race, simplejson.dumps(runnerDisconnectedModel))
    
  def send_finish(self, race, winner):
     self.sendToRunners(race, simplejson.dumps({ "messageType" : "finish", "payload" : str(winner)}))
    
  def reset_race(self, race):
     race.status = "lobby";
     race.put();
     
     for runner in race.runner_set:
        runner.delete()



