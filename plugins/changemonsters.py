from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class ChangeMonstersPlugin(WillPlugin):

    @route("/changemonsters/change", method="POST")
    def change_listener(self):
        payload = self.request.json

        if payload["form_class"] == "WalkForm":
            self.say(
                "@steven %(name)s set %(pronoun)s walk cues:\nCue: %(walk_cue)s\nRoutine: %(walk_routine)s\nReward: %(walk_reward)s \n %(localtime)s local time." %
                payload
            )
        elif payload["form_class"] == "BigMountainForm":
            self.say(
                "@steven %(name)s set their big mountain: By %(big_mountain_timeline)s, I will %(big_mountain_goal)s.\n %(localtime)s local time." %
                payload
            )
        elif payload["form_class"] == "checkin":
            self.say(
                "@steven %(name)s did their checkin!\nDid everything: %(did_everything)s\nDid walk: %(did_walk)s\nDid meditation: %(did_meditation)s\nDid slightlyscared: %(did_slightlyscared)s\n" %
                payload
            )
        elif payload["form_class"] == "email_sent":
            self.say(
                "@steven %(name)s's day %(day_number)s email was sent. \n %(body)s" %
                payload
            )
        else:
            self.say("@steven, I wasn't sure what to do with this: %s" % payload)
