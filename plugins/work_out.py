from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class SleepPlugin(WillPlugin):

    @route("/train/started")
    def training_start_listener(self):
        self.say("Steven's fired up endomondo!")

    @route("/train/stopped")
    def training_end_listener(self):
        self.say("Welcome back, @steven!")

