import datetime
import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template

class UptimePlugin(WillPlugin):
    
    def _verify_url(self, url):
        r = requests.get(url)
        if not r.status_code == 200:
            self.say("@all WARNING: %s is down! (%s code)" % (url, r.status_code))

    @periodic(second='5')
    def gk_is_up(self):
        self._verify_url("https://www.greenkahuna.com")
        self._verify_url("https://www.greenkahuna.com")