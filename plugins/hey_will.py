from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class HeyWillPlugin(WillPlugin):

    @route("/hey-will/", method='GET')
    @route("/hey-will/", method='POST')
    def hey_will_listener(self):
        try:
            print "hey_will_listener"
            print self
            print self.request
            print self.request.__dict__
            # print self.request.body
            print self.request.params
            if "phrase" in self.request.params:
                self.say(self.request.params["phrase"])
                return "You got it."
            else:
                return "Sorry, couldn't hear you!"
        except:
            return "Sorry, something went wrong!"
