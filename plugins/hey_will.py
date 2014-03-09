from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class HeyWillPlugin(WillPlugin):

    @route("/hey-will/")
    def hey_will_listener(self):
        try:
            if "phrase" in self.request.params:
                
                self.say(self.request.params["phrase"])
                return "You got it."
            else:
                return "Sorry, couldn't hear you!"
        except:
            return "Sorry, something went wrong!"
