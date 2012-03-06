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

import cgi
import os
import logging
import time

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import channel

from camelraces.model.race import Race
from camelraces.model.runner import Runner
from camelraces.service.race_service import RaceService

from django.utils import simplejson
from google.appengine.ext import webapp


class RunnerResource(webapp.RequestHandler):

    def __init__(self):
        self.raceService = RaceService()

    def post(self, runnerKey):
        jsonMessage = simplejson.loads(self.request.body);
        runner = Runner.get(runnerKey)
        
        {'gameUpdate': self.handleUpdate,
         'runnerStatusUpdate': self.handleReady}[jsonMessage["messageType"]](runner, jsonMessage)
     
    def handleReady(self, runner, jsonMessage):
        
        status = jsonMessage["payload"][str(runner.key())]
        runner.ready = status;
        runner.put();
        
        self.raceService.sendToRunners(runner.race, self.request.body)

        if (self.raceService.areAllRunnersReady(runner.race)):
            self.raceService.startRace(runner.race)

    def handleUpdate(self, runner, jsonMessage):
        winner = self.getWinner(jsonMessage);
        if (winner):
            race = runner.race
            race.status = "finished" #  TODO status should be a constant of the model
            race.put()
            self.raceService.send_finish(race, winner)
            return
        
        runner.position = jsonMessage["payload"][str(runner.key())];
        self.raceService.sendToRunners(runner.race, self.request.body)
        runner.put();
    
    def getWinner(self, update):
        for runnerKey in update["payload"]:
            if (update["payload"][runnerKey] > 100) :
                return Runner.get(runnerKey).user.nickname()
            
    