from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class SleepPlugin(WillPlugin):

    @route("/sleep/fell-asleep")
    def asleep_listener(self):
        self.say("Steven's going to sleep")

    @route("/sleep/woke-up")
    def awake_listener(self):
        self.say("G'morning, @steven!")
