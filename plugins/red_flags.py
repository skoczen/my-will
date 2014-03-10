import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings


class RedFlagsPlugin(WillPlugin):

    @periodic(hour='10', minute='0')
    def check_red_flags(self):

        # Drinking
        r = requests.get("http://stevenskoczen.com/manual/red-flags/drinking")
        if r.json()['too_much']:
            self.say("Red Flag!  You've had 3+ beers for the last 7 days.  Odds are very good you're depressed. Open up the manual page for depression, and let's get on this together. :)")