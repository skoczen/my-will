import random
from will.utils import Bunch

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
STACKS_KEY = "will.servers.stacks"


class Stack(Bunch):

    @property
    def adapter(self):
        if not hasattr(self, "_adapter"):
            self._adapter = HerokuAdapter(self)
        return self._adapter

    def ensure_created(self):
        return self.adapter.ensure_created()

    def deploy(self, branch):
        print "Deploying"
        return self.adapter.deploy()

    def destroy(self):
        print "destroying"
        return self.adapter.destroy()

    def get_monthly_cost(self):
        return self.adapter.get_monthly_cost()

    @property
    def title(self):
        return self.name.title()

    @property
    def id(self):
        return self.name.lower().replace(" ", "_")

    @property
    def url_name(self):
       return "gk-%s" % self.name.lower().replace(" ", "-")

    @property
    def url(self):
        return self.adapter.url

class HerokuAdapter(Bunch):
    def __init__(self, stack, *args, **kwargs):
        super(HerokuAdapter, self).__init__(*args, **kwargs)
        self.stack = stack

    def deploy(self, stack):
        print "deploy"

    def ensure_created(self):
        print "ensure_created"

    def destroy(self):
        print "destroying"

    def get_monthly_cost(self):
        print "get_monthly_cost"

    @property
    def url(self):
        return "https://%s.herokuapp.com" % (self.stack.url_name)

class ServersMixin(object):
    
    @property
    def stacks(self, force_load=False):
        if force_load or not hasattr(self, "_stacks"):
            self._stacks = self.load(STACKS_KEY, [])
        return self._stacks

    def save_stacks(self, stacks):
        self.save(STACKS_KEY, stacks)
        self._stacks = stacks

    def new_stack(self, branch):
        stacks = self.stacks
        new_name = self.get_unused_stack_name()
        new_stack = Stack(branch=branch, name=new_name)
        stacks.append(new_stack)
        self.save_stacks(stacks)
        return new_stack
   
    def destroy_stack(self, stack):
        stack.destroy()
        stacks = self.stacks
        new_stacks = []
        for s in stacks:
            if s.name != stack.name:
                new_stacks.append(s)
        self.save_stacks(new_stacks)

    def get_unused_stack_name(self):
        have_a_good_name = False
        while have_a_good_name is False:
            new_name = random.choice(BIGGEST_FISH_NAMES)
            have_a_good_name = True
            for stack in self.stacks:
                if stack.name == new_name:
                    have_a_good_name = False
        return new_name

    def get_stack_from_stack_name(self, stack_name):
        # Strict match
        for s in self.stacks:
            if s.name == stack_name:
                return s

        # Looser match
        for s in self.stacks:
            if s.id == stack_name or s.url_name == stack_name or s.id == stack_name:
                return s
        
        return None

    def get_stack_from_branch_name(self, branch_name):
        for s in self.stacks:
            if s.branch.name == branch_name or s.branch.name == "feature/%s" % (branch_name,):
                return Stack.restore_from_state(s)
        return None

    def prefixed_name(self, name):
        return "gk-%s" % name
