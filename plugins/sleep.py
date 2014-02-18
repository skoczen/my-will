from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class SleepPlugin(WillPlugin):

    @route("/sleep/fell-asleep")
    def asleep_listener(self, phrase):
        self.say("Steven's going to sleep")

    @route("/sleep/woke-up")
    def awake_listener(self, phrase):
        self.say("G'morning, @steven!")
