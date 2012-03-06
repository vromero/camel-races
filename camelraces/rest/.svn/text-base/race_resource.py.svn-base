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

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import channel
from google.appengine.ext import webapp
from camelraces.model.race import Race
from camelraces.model.runner import Runner

from django.utils import simplejson


class RaceResource(webapp.RequestHandler):

    def __init__(self):
        self.raceService = RaceService()
    
    def get(self, raceKey):
        race = Race.get(raceKey)
        runners = race.runner_set
    
        response = {}
        for runner in runners:
            email = str(runner.user)
            response[email] = runner.position
        
        self.response.out.write(simplejson.dumps(response))
    
      
