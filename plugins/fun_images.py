from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class FunImagesPlugin(WillPlugin):

    @hear("high(-| )(5|five)")
    def hear_highfive(self, message):
        self.say("https://gk-will.s3.amazonaws.com/highfive.jpg", message=message)

    @hear("bug")
    def hear_bug(self, message):
        self.say("https://gk-will.s3.amazonaws.com/bugfeature.gif", message=message)
