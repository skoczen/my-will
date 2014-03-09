import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


def todays_one_thing():
    r = requests.get("http://stevenskoczen.com/manual/one-thing/")
    return r.json()['one_thing']


class OneThingPlugin(WillPlugin):

    @respond_to("what's my one thing for today?")
    def respond_to_what_is(self, message):
        self.reply(message, todays_one_thing())

    @hear("^one thing")
    def hear_thanks(self, message):
        self.say(todays_one_thing(), message=message)
