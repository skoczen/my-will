from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class SleepPlugin(WillPlugin):

    @route("/sleep/fell-asleep")
    def asleep_listener(self):
        self.say("Steven's going to sleep")

    @route("/sleep/woke-up")
    def awake_listener(self):
        from one_thing import todays_one_thing
        self.say("G'morning, @steven!")
        # self.say("Today, %s" % todays_one_thing())
