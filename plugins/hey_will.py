from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class HeyWillPlugin(WillPlugin):

    @route("/hey-will/")
    def hey_will_listener(self):
        print self.request.body
        self.say(self.request.body)
        return "You got it."
