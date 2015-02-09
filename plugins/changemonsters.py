from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class ChangeMonstersPlugin(WillPlugin):

    @route("/changemonsters/change", method="POST")
    def change_listener(self):
        payload = self.request.json

        if payload["form_class"] == "WalkForm":
            self.say(
                "@steven %(name)s set %(pronoun)s walk cues:\nCue: %(walk_cue)ss\nRoutine: %(walk_routine)s\nReward: %(walk_reward)s" %
                payload
            )
        elif payload["form_class"] == "BigMountainForm":
            self.say(
                "@steven %(name)s set their big mountain: By %(big_mountain_timeline)s, I will %(big_mountain_goal)s." %
                payload
            )
        else:
            self.say("@steven, I wasn't sure what to do with this: %s" % payload)
