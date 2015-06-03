import datetime
from natural.date import delta
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from mixins.skoczen import SkoczenMixin

TRAINING_START_TIME_KEY = "training_start_time"
TRAINING_END_TIME_KEY = "training_end_time"
TRAINING_FLUID_RESPONSE_SENT_KEY = "training_fluid_response_sent"
TRAINING_START_WEIGHT_KEY = "training_start_weight"


class TrainPlugin(WillPlugin, SkoczenMixin):

    @route("/train/soon")
    def training_launch_listener(self):
        weigh_in = self.last_weigh_in()
        # Fired up endomondo
        last_15_minutes = datetime.datetime.now() - datetime.timedelta(minutes=15)
        if weigh_in["when"] < last_15_minutes:
            self.say("@steven don't forget to weigh in")

    @route("/train/started")
    def training_start_listener(self):
        self.say("Steven headed out!")
        self.save(TRAINING_START_TIME_KEY, datetime.datetime.now())
        weigh_in = self.last_weigh_in()
        self.save(TRAINING_START_WEIGHT_KEY, weigh_in)

    @route("/train/stopped")
    def training_end_listener(self):
        self.say("@steven Welcome back! Don't forget to weigh out.")
        self.save(TRAINING_END_TIME_KEY, datetime.datetime.now())
        self.save(TRAINING_FLUID_RESPONSE_SENT_KEY, False)

    @periodic(second="0")
    def training_summary(self):
        if self.load(TRAINING_FLUID_RESPONSE_SENT_KEY, None) is False:
            start_weight = self.load(TRAINING_START_WEIGHT_KEY)
            weigh_in = self.last_weigh_in()
            if weigh_in["when"] != start_weight["when"]:
                start_time = self.load(TRAINING_START_TIME_KEY)
                end_time = self.load(TRAINING_END_TIME_KEY)
                time = "who knows how"
                if start_time and end_time:
                    time = delta(start_time, end_time)[0]

                pounds_difference = weigh_in["weight"] - start_weight["weight"]
                ounces = pounds_difference * 16

                self.say("Last training was %s long, with %s oz fluid loss. Drink up!" % (time, ounces))
                self.clear(TRAINING_START_TIME_KEY)
                self.clear(TRAINING_END_TIME_KEY)
                self.save(TRAINING_FLUID_RESPONSE_SENT_KEY, True)

    # @periodic(hour=17, minute=0, second=0)
    # def check_weight(self):
    #     self.last_weigh_in()

    @respond_to("weight$")
    def last_weight(self, message):
        last_weight = self.last_weigh_in()
        self.say("Last weight was %s lbs, %s%%, %s" % (
            last_weight["weight"],
            last_weight["fat"],
            self.to_natural_day_and_time(last_weight["when"])
        ))

    @respond_to("weights$")
    def last_weights(self, message):
        weights = self.weights()
        status_text = rendered_template("weights.html", {"weights": weights})
        self.say(status_text, message=message, html=True)

    @respond_to("cancel workout")
    def cancel_workout(self, message):
        self.clear(TRAINING_START_TIME_KEY)
        self.clear(TRAINING_END_TIME_KEY)
        self.save(TRAINING_FLUID_RESPONSE_SENT_KEY, True)
        self.say("Done.", message=message)
