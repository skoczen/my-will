from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from mixins.skoczen import SkoczenMixin


class OneThingPlugin(WillPlugin, SkoczenMixin):

    @respond_to("what's my one thing(?: for today)?")
    def respond_to_what_is(self, message):
        self.reply(message, self.todays_one_thing())

    @respond_to("^one thing")
    def hear_thanks(self, message):
        one_thing = self.todays_one_thing()
        one_thing = "%s%s" % (one_thing[0].upper(), one_thing[1:])
        self.say(one_thing, message=message)

    # @periodic(hour='11', minute='0')
    # def say_todays_thing(self):
    #     self.say("@steven Today's one thing: %s" % self.todays_one_thing())
