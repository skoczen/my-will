import random

import heroku
import requests

from will.utils import Bunch
from will import settings

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

    def deploy(self, new_config):
        print "Deploying"
        self.branch.deploy_config = new_config
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

    @property
    def deploy_config(self):
        return self.branch.deploy_config

class HerokuAdapter(Bunch):
    def __init__(self, stack, *args, **kwargs):
        super(HerokuAdapter, self).__init__(*args, **kwargs)
        self.stack = stack
        self.heroku = heroku.from_key(settings.WILL_HEROKU_API_KEY)

    def deploy(self, code_only=False):
        self.ensure_created()
        print "deploy, code_only=%s" % code_only

        if not code_only:
        # DB
            if "cloned_database" in self.stack.deploy_config["heroku"]:
                # Undocumented API via heroku gem code:
                # https://github.com/heroku/heroku/blob/master/lib/heroku/client/pgbackups.rb
                # import requests
                # from will import settings
                # data = {
                #     "user": settings.WILL_HEROKU_API_KEY,
                #     "password": ""
                # }
                # r = requests.get("https://api.heroku.com/client/latest/backup", data=data)
                # print r.status_code
                # print r.json()
                # Get latest
                # /client/latest_backup"
                
                # "heroku pgbackups:capture --app %s" % self.stack.deploy_config["heroku"]["cloned_database"]
                # "url = `heroku pgbackups:url` --app %s" % self.stack.deploy_config["heroku"]["cloned_database"]
                # "heroku pgbackups:restore --app %s" % self.stack.url_name
                pass

        # Push code

        # Scale

    def ensure_created(self):
        creating = False
        try:
            # Get or create the app
            try:
                self.app = self.heroku.apps[self.stack.url_name]
            except:
                creating = True
                self.app = self.heroku.apps.add(self.stack.url_name)

            print "self.app.addons: %s" % self.app.addons
            print "self.app.config: %s" % self.app.config
            self.addons = [k.name for k in self.app.addons]
            print "self.addons: %s" % self.addons
            
            cached_config = dict(self.app.config.data)
            print "cached_config: %s" % cached_config

            # Addons
            if "addons" in self.stack.deploy_config["heroku"]:
                for addon in self.stack.deploy_config["heroku"]["addons"]:
                    if addon not in self.addons:
                        print addon
                        self.app.addons.add(addon)
                for addon_name in self.addons:
                    if addon_name not in self.stack.deploy_config["heroku"]["addons"]:
                        del self.app.addons[addon_name]

            # Static Config
            if "config" in self.stack.deploy_config["heroku"]:
                for k, v in self.stack.deploy_config["heroku"]["config"].items():
                    if k not in cached_config or cached_config[k] != v:
                        v = v.replace("$APP_NAME", self.stack.url_name)
                        self.app.config[k] = v

            # Cloned config
            if "cloned_config" in self.stack.deploy_config["heroku"]:
                for app in self.stack.deploy_config["heroku"]["cloned_config"]:
                    other_app = self.heroku.apps[app]
                    other_cached_config = dict(other_app.config.data)
                    for k in self.stack.deploy_config["heroku"]["cloned_config"][app]:
                        if (k not in cached_config or 
                            (k in other_cached_config and cached_config[k] != other_cached_config[k])):
                            print "%s=%s" % (k, other_cached_config[k])
                            self.app.config[k] = other_cached_config[k]

        except Exception, e:
            import traceback; traceback.print_exc();
            if creating:
                self.destroy()
            raise e

    def destroy(self):
        try:
            app = self.heroku.apps[self.stack.url_name]
            app.destroy()
        except KeyError:
            # It's already been deleted.
            pass

    def get_monthly_cost(self):
        print "get_monthly_cost"

    @property
    def url(self):
        return "https://%s.herokuapp.com" % (self.stack.url_name)

class ServersMixin(object):
    
    @property
    def stacks(self):
        return self.load(STACKS_KEY, {})

    def save_stacks(self, stacks):
        self.save(STACKS_KEY, stacks)
        self._stacks = stacks

    def new_stack(self, branch):
        stacks = self.stacks
        new_name = self.get_unused_stack_name()
        new_stack = Stack(branch=branch, name=new_name)
        stacks[new_stack.id] = new_stack
        self.save_stacks(stacks)
        # This comes after, so that even if it blows up, will knows
        # about the stack (it might be partially there, and still
        # charging us.)
        new_stack.ensure_created()
        return new_stack
   
    def deploy(self, stack, code_only=False):
        config = self.get_deploy_config_for_branch(stack.branch.name)
        stack.deploy(config, code_only=code_only)

    def destroy_stack(self, stack):
        stack.destroy()
        stacks = self.stacks
        del stacks[stack.id]
        self.save_stacks(stacks)
        self._stacks = stacks

    def get_unused_stack_name(self):
        have_a_good_name = False
        while have_a_good_name is False:
            new_name = random.choice(BIGGEST_FISH_NAMES)
            have_a_good_name = True
            for stack_id, stack in self.stacks.items():
                if stack.name == new_name:
                    have_a_good_name = False
        return new_name

    def get_stack_from_stack_name(self, stack_name):
        # ID match
        if stack_name in self.stacks:
            return self.stacks[stack_name]

        # Strict match
        for stack_id, s in self.stacks.items():
            if s.name == stack_name:
                return s
        

        # Looser match
        for stack_id, s in self.stacks.items():
            if s.id == stack_name or s.url_name == stack_name or s.id == stack_name:
                return s
        
        return None

    def get_stack_from_branch_name(self, branch_name):
        for s_id, s in self.stacks.items():
            if s.branch.name == branch_name or s.branch.name == "feature/%s" % (branch_name,):
                return Stack.restore_from_state(s)
        return None

    def prefixed_name(self, name):
        return "gk-%s" % name
