from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class HeyWillPlugin(WillPlugin):

    @route("/hey-will/(?P<phrase>.*)")
    def hey_will_listener(self, phrase):
        self.say(phrase)
