import datetime
import requests
from random import choice

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class SpinTheWheelPlugin(WillPlugin):

    def get_temp(self, message):
        city_id = 0

        if "Steven Skoczen" in str(message["from"]):
            # Barcelona -> 3128760
            # Paris -> 2988507
            city_id = 5746545

        if "Levi Thomason" in str(message["from"]) or "Eric Carmichael" in str(message["from"]):
            city_id = 5590453

        r = requests.get("http://api.openweathermap.org/data/2.1/weather/city/%s?units=imperial" % city_id)

        return r.json()["main"]["temp"]

    def is_it_warm_outside(self, message):
        temp = self.get_temp(message)

        return temp > 55

    def is_it_cold_outside(self, message):
        return not self.is_it_warm_outside(message)

    @respond_to("^spin the wheel")
    def spin_the_wheel(self, message):
        print self.is_it_warm_outside(message)

        options = [
            "call an old friend",
            "go for a walk"
        ]

        if "Eric Carmichael" in str(message["from"]):
            options += [
                "pickup a book that you forgot the ending to",
                "play with the dog and cats",
                "max out squat weight",
                "squat 'til you drop",
                "workout your arms",
                "stretch your legs",
                "how many pull ups can you do? 3 sets to do as many as you can"
            ]

            if self.is_it_cold_outside(message):
                options += [
                    "drink some hot cocoa",
                    "make some chicken noodle soup from scratch",
                    "fly a toy helicopter"
                ]
            else:
                options += [
                    "go for a run",
                    "find a mushroom",
                    "find an animal"
                ]

        if "Steven Skoczen" in str(message["from"]):
            options += [
                "write about your day from the perspective of a 15 year old version of yourself",
                "write a poem",
                "pickup a book where you have forgotten exactly what happens at the end",
            ]

        if "Levi Thomason" in str(message["from"]):
            options += [
                "ask a collegue for something interesting to research",
                "sketch an example logo for GK",
                "learn a new photoshop/illustrator tutorial"
            ]

        self.reply(message, choice(options))















