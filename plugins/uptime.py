import requests
import time
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class UptimePlugin(WillPlugin):

    def _verify_url(self, url):
        try:
            r = requests.get(url)
            if not r.status_code == 200:
                time.sleep(5)
                r = requests.get(url)
                if not r.status_code == 200:
                    self.say("@all WARNING: %s is down! (%s code)" % (url, r.status_code), color="red")
        except:
            pass

    @periodic(second='5')
    def ss_is_up(self):
        self._verify_url("http://stevenskoczen.com")

    @periodic(second='5')
    def slowart_is_up(self):
        self._verify_url("http://slowartpdx.com")

    @periodic(second='5')
    def encore_is_up(self):
        self._verify_url("http://encorepoem.com")

    @periodic(second='5')
    def autoscalebot_is_up(self):
        self._verify_url("https://www.autoscalebot.com")

    @periodic(second='5')
    def goodcloud_is_up(self):
        self._verify_url("http://www.agoodcloud.com")

    @periodic(second='5')
    def isenough_is_up(self):
        self._verify_url("http://isenough.com")

    @periodic(second='5')
    def sixlinks_is_up(self):
        self._verify_url("http://sixlinks.org")