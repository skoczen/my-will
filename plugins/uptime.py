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
    def inkandfeet_is_up(self):
        self._verify_url("http://www.inkandfeet.com")

    @periodic(second='5')
    def inkandfeetblog_is_up(self):
        self._verify_url("http://blog.inkandfeet.com")

    @periodic(second='5')
    def lifeplan_is_up(self):
        self._verify_url("https://two-year-life-plan.teachery.co")

    # @periodic(second='5')
    # def footprints_is_up(self):
    #     self._verify_url("http://footprintsapp.com")

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
    def changemonsters_is_up(self):
        self._verify_url("http://thechangemonsters.com/")


    @periodic(second='5')
    def isenough_is_up(self):
        self._verify_url("http://isenough.com")

    @periodic(second='5')
    def poemhub_is_up(self):
        self._verify_url("http://poemhub.org")

    @periodic(second='5')
    def sixlinks_is_up(self):
        self._verify_url("http://sixlinks.org")

    @periodic(second='5')
    def coffeehouses_is_up(self):
        self._verify_url("http://coffeehous.es")

    # @periodic(second='5')
    # def correlationbot_is_up(self):
    #     self._verify_url("http://correlationbot.com")

    # @periodic(second='5')
    # def spicegrove_is_up(self):
    #     self._verify_url("http://www.spicegrovedesigns.com")
