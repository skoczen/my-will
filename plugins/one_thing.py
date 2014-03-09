import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


def todays_one_thing():
    r = requests.get("http://stevenskoczen.com/manual/one-thing/")
    return r.json()['one_thing']


class OneThingPlugin(WillPlugin):

    @respond_to("what's my one thing(?: for today)?")
    def respond_to_what_is(self, message):
        self.reply(message, todays_one_thing())

    @respond_to("^one thing")
    def hear_thanks(self, message):
        one_thing = todays_one_thing()
        one_thing = "%s%s" % (one_thing[0].upper(), one_thing[1:])
        self.say(one_thing, message=message)
