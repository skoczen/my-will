import random

BIGGEST_FISH_NAMES = [
    "coelacanth",
    "lungfish",
    "ocean sunfish",
    "beluga",
    "sturgeon",
    "chinese paddlefish",
    "kaluga",
    "bowfin",
    "conger",
    "lancetfish",
    "tigerfish",
    "giant barb",
    "atlantic cod",
    "alligator gar",
    "goosefish",
    "arapaima",
    "black marlin",
    "blue marlin",
    "bluefin tuna",
    "swordfish",
    "halibut",
    "chinook",
    "taimen",
    "mekong giant catfish",
    "wels catfish",
    "tiger shark",
    "whale shark",
    "sixgill shark",
    "basking shark",
    "great white shark",
    "megalodon",
    "manta ray",
    "sawfish",
    "giant guitarfish",
    "greenland shark",
    "angelshark",
    "atlantic torpedo",
]

class ServersMixin(object):
    
    @property
    def stacks(self, force_load=False):
        if force_load or not hasattr(self, "_stacks"):
            self._stacks = self.load("will.servers.stacks", [])
        return self._stacks

    def get_unused_stack_name(self):
        have_a_good_name = False
        while have_a_good_name is False:
            new_name = random.choice(BIGGEST_FISH_NAMES)
            have_a_good_name = True
            for stack in self.stacks:
                if stack.name == new_name:
                    have_a_good_name = False
        return {
            "url": "gk-%s" % new_name.replace(" ", "-"),
            "title": new_name.title(),
            "name": new_name,
        }

