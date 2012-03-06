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
from google.appengine.ext.webapp.util import run_wsgi_app

from camelraces.web.runner_controller import RunnerController
from camelraces.web.race_controller import RaceController
from camelraces.web.race_controller import RacePodiumRequestHandler
from camelraces.web.welcome_controller import WelcomeRequestHandler
from camelraces.web.presence_controller import DisconnectedController

application = webapp.WSGIApplication(
                                     [('/', WelcomeRequestHandler),
                                      (r'/race/(.*)/podium', RacePodiumRequestHandler),
                                      (r'/race/(.*)/runner/(.*)', RunnerController),
                                      ('/race/(.*)', RaceController),
                                      ('/race', RaceController),
                                      ('/_ah/channel/disconnected/', DisconnectedController)
                                      ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

