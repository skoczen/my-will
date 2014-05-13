from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings

class MonthlyGoalsPlugin(WillPlugin):

    @respond_to("Set my monthly goals to (?P<goals>.*)", multiline=True)
    def set_goals(self, message, goals=""):
        print "goals: %s" % goals
        self.save("monthly_goals", goals)
        self.say("Got it.", message=message)

    @periodic(hour='9', minute='0', day_of_week="mon")
    def say_goals_on_monday(self):
        self.say_goals()

    @respond_to("^(?:What are my )?(?:monthly )?goals")
    def respond_to_goals_question(self, message):
        self.say_goals(message=message)


    def say_goals(self, message=None):
        goals = self.load("monthly_goals", False)
        if goals:
            self.say("@all our monthly goals:\n %s" % goals, message=message)
        else:
            self.say("No monthly goals set.", message=message)

    @periodic(hour='10', minute='30',)
    def reminder_morning_mood(self):
        self.say("@all What's your morning mood?")
