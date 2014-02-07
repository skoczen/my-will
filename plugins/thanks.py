from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class ThanksPlugin(WillPlugin):

    @respond_to("^(?:thanks|thank you|tx|thx)")
    def respond_to_thanks(self, message):
        self.reply(message, "You're welcome!")

    @hear("thanks,? will")
    def hear_thanks(self, message):
        self.say("You're welcome!", message=message)