import datetime
import requests
import random

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class SpinTheWheelPlugin(WillPlugin):

    def __init__(self):
        self.random = random.Random()

    def get_temp(self, message):
        city_id = 0

        if "Steven Skoczen" in str(message.sender.nick):
            # Barcelona -> 3128760
            # Paris -> 2988507
            city_id = 5746545

        if "Levi Thomason" in str(message.sender.nick) or "Eric Carmichael" in str(message.sender.nick):
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
        options = [
            "call an old friend",
            "go for a walk",
            "compliment your significant other",
        ]

        if "Eric Carmichael" in str(message.sender.name):
            options += [
                "go for a run",
                "levi buys eric (coffee)!",
                "pickup a book that you forgot the ending to",
                "play with the dog and cats",
                "max out squat weight",
                "squat 'til you drop",
                "workout your arms",
                "stretch your legs",
                "how many pull ups can you do? 3 sets to do as many as you can",
            ]

            if self.is_it_cold_outside(message):
                options += [
                    "drink some hot cocoa",
                    "make some chicken noodle soup from scratch",
                    "fly a toy helicopter"
                ]
            else:
                options += [
                    "find a mushroom",
                    "find an animal"
                ]

        if "Steven Skoczen" in str(message.sender.name):
            options += [
                "write about your day from the perspective of a 15 year old version of yourself",
                "pickup a book where you have forgotten exactly what happens at the end",
                "take Tomo for a walk",
                "plan an item on the year list",
                "read one poem",
                "review my GK notifications",
                "clean/dust something that doesn't normally get cleaned"
            ]

        if "Levi Thomason" in str(message.sender.name):
            options += [
                "ask a collegue for something interesting to research",
                "sketch an example logo for GK",
                "learn a new photoshop/illustrator tutorial",
                "eric buys levi (coffee)!",
                "post an item on some major site (ebay, craigslist, instagram, etc.)",
                "create an account and profile on some site for construction companies",
                "use an old feature on the live site",
                "use a new feature on the live site",
            ]

            if self.is_it_warm_outside(message):
                options += [
                    "toss the frizz"
                ]

        self.reply(message, self.random.choice(options))















