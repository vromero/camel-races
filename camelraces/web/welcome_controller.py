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
 
class WelcomeRequestHandler(webapp.RequestHandler):
    """ This request handler manages the landing page """
    
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'  # TODO THIS SHOULD BE I18Ned
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'  # TODO THIS SHOULD BE I18Ned
    
        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'logged' : True if users.get_current_user() else False
        }
      
        path = os.path.join(os.path.dirname(__file__), '../../templates/welcome.html')
        self.response.out.write(template.render(path, template_values))
    
