import datetime
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class CYFIsEvilPlugin(WillPlugin):

    @hear("\(cyf\)")
    def scream_from_cyf(self, message):
        self.say("NOOOOOOOooooooOOOOOO!!!  It huurts!!")
