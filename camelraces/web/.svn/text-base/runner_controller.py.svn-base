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

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

from camelraces.model.race import Race
from camelraces.model.runner import Runner

import os
import logging

class RunnerController(webapp.RequestHandler):
    
    def get(self, raceKey, runnerKey):
        """ Returns the portion of html needed to represent a runner """
        runner = Runner.get(runnerKey)
        
        ret = {"runner" : {
                'runner_key': str(runner.key()),
                'runner_name': runner.user.nickname(), 
                'runner_position': runner.position,
                'runner_visible' : False,
                'runner_ready' : runner.ready
          }};

        path = os.path.join(os.path.dirname(__file__), '../../templates/show-race-player.html')
        self.response.out.write(template.render(path, ret))
        
