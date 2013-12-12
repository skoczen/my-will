import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings

keep_alive_url = "/keep-alive"
class PeriodicTestPlugin(WillPlugin):

    @periodic(second=0)
    def ping_keep_alive(self):
        print "ping_keep_alive called" 
        requests.get("%s%s" % (settings.WILL_URL, keep_alive_url))
