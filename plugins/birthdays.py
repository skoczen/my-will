from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class BirthdayPlugin(WillPlugin):

    @periodic(month="4", day="9", minute="0", hour="0")
    def happy_birthday_from_will(self):
        self.say("@steven Happy Birthday!!!! :)")
