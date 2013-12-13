from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class SayPlugin(WillPlugin):

    @route("/say/<phrase>")
    def say(self, phrase):
        self.say(phrase)
