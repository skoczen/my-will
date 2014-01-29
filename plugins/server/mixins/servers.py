import base64
import fcntl
import os
import random
import requests
import shutil
import subprocess
import time

import heroku

from will.mixins import StorageMixin
from will.utils import Bunch
from will import settings

BIGGEST_FISH_NAMES = [
    "lungfish",
    "sunfish",
    "beluga",
    "sturgeon",
    "paddlefish",
    "kaluga",
    "bowfin",
    "conger",
    "lancetfish",
    "tigerfish",
    "atlantic cod",
    "goosefish",
    "arapaima",
    "black marlin",
    "blue marlin",
    "bluefin tuna",
    "swordfish",
    "halibut",
    "chinook",
    "taimen",
    "giant catfish",
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
COLLABORATOR_EMAILS = [
    "eric@greenkahuna.com",
    "levi@greenkahuna.com",
    "steven@greenkahuna.com",
    "will@greenkahuna.com",
]
STACKS_KEY = "will.servers.stacks"

def non_blocking_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return None


class Stack(Bunch):

    @property
    def adapter(self):
        if not hasattr(self, "_adapter"):
            self._adapter = HerokuAdapter(self)
        return self._adapter

    def ensure_created(self):
        return self.adapter.ensure_created()

    def deploy(self, new_config, code_only=False, force=False):
        print "Deploying"
        self.branch.deploy_config = new_config
        return self.adapter.deploy(code_only=code_only, force=force)

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
       return "%s%s" % (settings.WILL_DEPLOY_PREFIX, self.name.lower().replace(" ", "-"))

    @property
    def url(self):
        return self.adapter.url

    @property
    def deploy_config(self):
        return self.branch.deploy_config

    @property
    def deploy_output_key(self):
        return "deploy_output_%s" % self.id

    @property
    def deploy_log_url(self):
        return "%s/deploy-log/%s" % (settings.WILL_URL, self.id)

    @property
    def active_deploy_key(self):
        return "active_deploy_%s" % self.id

class HerokuAdapter(Bunch, StorageMixin):
    def __init__(self, stack, *args, **kwargs):
        super(HerokuAdapter, self).__init__(*args, **kwargs)
        self.stack = stack
        self.heroku = heroku.from_key(settings.WILL_HEROKU_API_KEY)

    def ensure_cli_auth(self):
        cli_auth_path = os.path.abspath(os.path.expanduser("~/.will_cli_auth"))
        if not os.path.exists(cli_auth_path):
            netrc_path = os.path.abspath(os.path.expanduser("~/.netrc"))
            if not os.path.exists(netrc_path):
                with open(netrc_path, 'w+') as f:
                    f.write("""
machine api.heroku.com
  login %(email)s
  password %(token)s
machine code.heroku.com
  login %(email)s
  password %(token)s
    """ % {
            "email": settings.WILL_HEROKU_EMAIL,
            "token": settings.WILL_HEROKU_API_KEY,
        })
            ssh_dir = os.path.abspath(os.path.expanduser("~/.ssh"))
            if not os.path.exists(ssh_dir):
                os.makedirs(ssh_dir)

            ssh_config_path = os.path.abspath(os.path.expanduser("~/.ssh/config"))
            if not os.path.exists(ssh_config_path):
                with open(ssh_config_path, 'w+') as f:
                    f.write("""
UserKnownHostsFile /dev/null
StrictHostKeyChecking no
""")

            id_rsa_path = os.path.abspath(os.path.expanduser("~/.ssh/will_id_rsa"))
            if not os.path.exists(id_rsa_path):
                with open(id_rsa_path, 'w+') as f:
                    f.write(settings.WILL_SSH.replace(";;", "\n"))

            id_rsa_pub_path = os.path.abspath(os.path.expanduser("~/.ssh/will_id_rsa.pub"))
            if not os.path.exists(id_rsa_pub_path):
                with open(id_rsa_pub_path, 'w+') as f:
                    f.write(settings.WILL_SSH_PUB)

            self.run_command("chmod 600 will_id_rsa", cwd=ssh_dir, auth_first=False)

            with open(cli_auth_path, 'w+') as f:
                f.write("Done")

    def command_with_ssh(self, command):
        return 'ssh-agent bash -c "ssh-add ~/.ssh/will_id_rsa; %s 2>&1"' % command.replace('"', r'\"')

    def add_to_saved_output(self, additional_output, with_newline=True):
        output = self.load(self.stack.deploy_output_key, "")
        if with_newline:
            output = "%s%s\n" % (output, additional_output)
        else:
            output = "%s%s" % (output, additional_output)
        self.save(self.stack.deploy_output_key, output)

    def run_subprocess_with_saved_output(self, command,):
        output = self.load(self.stack.deploy_output_key, "")
        output = "%s\n" % output
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        
        while p.poll() is None:
            line = non_blocking_read(p.stdout)
            if line:
                if line[:len("Identity added: ")] != "Identity added: ":
                    output = "%s%s" % (output, line)
                    self.save(self.stack.deploy_output_key, output)
            time.sleep(1)

        try:
            changed = False
            out, err = p.communicate()
            if out:
                out = out.replace("\r", "")
                output = "%s\n%s" % (output, out)
                changed = True
            if err:
                err = err.replace("\r", "")
                output = "%s\n%s" % (output, err)
                changed = True
        except ValueError:
            pass

        if changed:
            self.save(self.stack.deploy_output_key, output)

        if p.returncode != 0:
            output = '%s\n\n======================\nError running %s' % (output, command)
            self.save(self.stack.deploy_output_key, output)
            raise Exception("Error running %s" % command)

    def run_heroku_cli_command(self, command, app=None, stream_output=True, cwd=None):
        self.ensure_cli_auth()
        if not "--app" in command and not "-a " in command:
            if app:
                command = "%s --app %s" % (command, app)
            else:
                command = "%s --app %s" % (command, self.stack.url_name)
        command = self.command_with_ssh("heroku %s" % command)

        if cwd:
            command = "cd %s; %s" % (cwd, command)
        print "running %s" % command
        if not stream_output:
            return subprocess.check_output(command, shell=True)
        else:
            return self.run_subprocess_with_saved_output(command)

    def run_command(self, command, cwd=None, stream_output=True, auth_first=True):
        if auth_first:
            self.ensure_cli_auth()
        if cwd:
            command = "cd %s; %s" % (cwd, command)
        command = self.command_with_ssh(command)
        print "running %s" % command
        if not stream_output:
            return subprocess.check_output(command, shell=True)
        else:
            return self.run_subprocess_with_saved_output(command)

    def get_code_dir(self):
        """Get a unique dir for this stack for holding the code (should speed up redeploys)"""

        base_code_dir = os.path.abspath(os.path.expanduser("~/.will_codebases"))

        if not os.path.exists(base_code_dir):
            os.makedirs(base_code_dir)

        stack_code_dir = os.path.join(base_code_dir, self.stack.id)
        if not os.path.exists(stack_code_dir):
            os.makedirs(stack_code_dir)
        return stack_code_dir

    def deploy(self, code_only=False, force=False):
        if self.load(self.stack.active_deploy_key, False) and not force:
            raise Exception("Deploy already in progress!")
        else:
            self.save(self.stack.active_deploy_key, True)
            try:
                self.ensure_created()

                if not code_only:
                    # Clone the DB
                    if "cloned_database" in self.stack.deploy_config["heroku"]:
                        self.add_to_saved_output("Cloning the database:")
                        self.run_heroku_cli_command("pgbackups:capture --app %s --expire" % self.stack.deploy_config["heroku"]["cloned_database"])
                        self.add_to_saved_output(" - New backup made.")
                        url = self.run_heroku_cli_command("pgbackups:url --app %s" % self.stack.deploy_config["heroku"]["cloned_database"], stream_output=False).replace("\n","")
                        self.add_to_saved_output(" - URL verified.")
                        cached_config = dict(self.app.config.data)
                        stack_db_config_name = "DATABASE"
                        for k,v in cached_config.items():
                            if "HEROKU_POSTGRESQL_" in k:
                                stack_db_config_name = k
                                break
                        self.run_heroku_cli_command("pgbackups:restore %s --app %s --confirm %s %s " % (stack_db_config_name, self.stack.url_name, self.stack.url_name, url, ))
                        self.add_to_saved_output(" - Database restored.")

                # Push code
                code_dir = self.get_code_dir()
                repo_dir = os.path.join(self.get_code_dir(), "repo")
                
                # Make sure we have the code
                if not os.path.exists(os.path.join(repo_dir, ".git", "config")):
                    self.add_to_saved_output("Cloning codebase:")
                    self.run_command("git clone %s repo" % self.stack.branch.repo_clone_url, cwd=code_dir)
                    self.run_command("git remote add heroku git@heroku.com:%s.git" % self.stack.url_name, cwd=repo_dir)

                self.add_to_saved_output("Updating code:")
                self.add_to_saved_output(" - fetching origin... ", with_newline=False)
                self.run_command("git fetch origin %s" % self.stack.branch.name, cwd=repo_dir, stream_output=False)
                self.add_to_saved_output("done.")
                self.add_to_saved_output(" - checking out %s... " % self.stack.branch.name, with_newline=False)
                self.run_command("git checkout %s" % self.stack.branch.name, cwd=repo_dir, stream_output=False)
                self.add_to_saved_output("done.")
                self.add_to_saved_output(" - pulling latest changes... ", with_newline=False)
                self.run_command("git pull", cwd=repo_dir, stream_output=False)
                self.add_to_saved_output("done.")

                # Push to heroku
                self.add_to_saved_output("Pushing to heroku:")
                self.run_command("git push heroku %s:master --force" % self.stack.branch.name, cwd=repo_dir)

                # Post-deploy hooks
                if "post_deploy" in self.stack.deploy_config["heroku"]:
                    self.add_to_saved_output("Running post-deploy commands:")
                    post_deploy_command_types = self.stack.deploy_config["heroku"]["post_deploy"]
                    if "heroku" in post_deploy_command_types:
                        for cmd in post_deploy_command_types["heroku"]:
                            self.add_to_saved_output(" - heroku %s" % cmd)
                            self.run_heroku_cli_command(cmd, cwd=repo_dir)
                    if "shell" in post_deploy_command_types:
                        for cmd in post_deploy_command_types["shell"]:
                            self.add_to_saved_output(" - %s" % cmd)
                            self.run_command(cmd, cwd=repo_dir)

                
                # Scale
                if "scale" in self.stack.deploy_config["heroku"]:
                    self.add_to_saved_output("Scaling:")
                    for service, num_workers in self.stack.deploy_config["heroku"]["scale"].items():
                        self.run_heroku_cli_command("scale %s=%s" % (service, num_workers))
                        self.add_to_saved_output("- %s=%s" % (service, num_workers))
                
                self.add_to_saved_output("Deploy complete")
                self.add_to_saved_output('<a href="%s">%s</a>' % (self.stack.url, self.stack.url))
                self.save(self.stack.active_deploy_key, False)
            except:
                self.save(self.stack.active_deploy_key, False)
                raise

    def ensure_collaborators(self):
        self.add_to_saved_output("Ensuring collaborators:")
        self.collaborators = [c.email for c in self.app.collaborators]
        print self.collaborators
        print [c.__dict__ for c in self.app.collaborators]

        for c in COLLABORATOR_EMAILS:
            self.add_to_saved_output(" - %s" % c)
            print self.app.collaborators
            if not c in self.collaborators:
                auth_token = base64.b64encode("%s:%s" % (settings.WILL_HEROKU_EMAIL, settings.WILL_HEROKU_API_KEY))
                data = {
                    "user": c,
                    "silent": True,
                }
                headers = {
                    'Content-type': 'application/json',
                    'Accept': 'application/vnd.heroku+json',
                    'version': 3,
                    'Authorization': 'Basic %s' % auth_token,
                }
                print data
                print headers
                r = requests.post(
                    "https://api.heroku.com/apps/%s/collaborators" % self.stack.url_name,
                    headers=headers,
                    data=data,
                )
                print r
                if not r.status_code == 200:
                    raise Exception("Unable to add %s as a collaborator. (%s)" % (c, r.status_code))

    def ensure_created(self):
        self.save(self.stack.deploy_output_key, "")
        creating = False
        try:
            # Get or create the app
            try:
                self.app = self.heroku.apps[self.stack.url_name]
                self.add_to_saved_output("App exists: %s" % self.stack.url_name)
            except:
                creating = True
                forked = False
                if "fork" in self.stack.deploy_config["heroku"]:
                    self.run_heroku_cli_command("fork -a %s %s" % (self.stack.deploy_config["heroku"]["fork"], self.stack.url_name))
                    self.add_to_saved_output("Forked to new app: %s" % self.stack.url_name)
                    self.app = self.heroku.apps[self.stack.url_name]
                    forked = True
                else:
                    self.app = self.heroku.apps.add(self.stack.url_name)
                    self.add_to_saved_output("Created new app: %s" % self.stack.url_name)

            self.addons = [k.name for k in self.app.addons]
            cached_config = dict(self.app.config.data)
            
            # Collaborators
            self.ensure_collaborators()

            # Labs
            if "labs" in self.stack.deploy_config["heroku"]:
                self.add_to_saved_output("Configuring Labs")
                lab_config = self.run_heroku_cli_command("labs", stream_output=False)
                for lab_feature in self.stack.deploy_config["heroku"]["labs"]:
                    self.add_to_saved_output(" - %s" % lab_feature)
                    enabled_str = "[+] %s" % lab_feature
                    if not enabled_str in lab_config:
                        self.run_heroku_cli_command("labs:enable %s" % (lab_feature,))
                for lab_feature in lab_config.split("\n"):
                    if lab_feature[:3] == "[+]":
                        feature_name = lab_feature[4:lab_feature.find(" ",5)]
                        print "enabled: %s" % feature_name
                        if feature_name not in self.stack.deploy_config["heroku"]["labs"]:
                            self.add_to_saved_output(" - %s (removed)" % feature_name)
                            self.run_heroku_cli_command("labs:disable %s --confirm %s" % (lab_feature, self.stack.url_name))

            # Addons
            if "addons" in self.stack.deploy_config["heroku"]:
                self.add_to_saved_output("Configuring addons:")
                for addon in self.stack.deploy_config["heroku"]["addons"]:
                    self.add_to_saved_output(" - %s" % addon)
                    if addon not in self.addons:
                        print addon
                        self.app.addons.add(addon)
                for addon_name in self.addons:
                    if addon_name not in self.stack.deploy_config["heroku"]["addons"]:
                        self.run_heroku_cli_command("addons:remove %s --confirm %s" % (addon_name, self.stack.url_name))
                        self.add_to_saved_output(" - %s (removed)" % addon)

            # Static Config
            if "config" in self.stack.deploy_config["heroku"]:
                self.add_to_saved_output("Configuring environment:")
                for k, v in self.stack.deploy_config["heroku"]["config"].items():
                    self.add_to_saved_output(" - %s" % k)
                    if k not in cached_config or cached_config[k] != v:
                        v = v.replace("$APP_NAME", self.stack.url_name)
                        self.app.config[k] = v

            # Cloned config
            if "cloned_config" in self.stack.deploy_config["heroku"]:
                for app in self.stack.deploy_config["heroku"]["cloned_config"]:
                    other_app = self.heroku.apps[app]
                    other_cached_config = dict(other_app.config.data)
                    for k in self.stack.deploy_config["heroku"]["cloned_config"][app]:
                        self.add_to_saved_output(" - %s" % k)
                        if (k not in cached_config or 
                            (k in other_cached_config and cached_config[k] != other_cached_config[k])):
                            print "%s=%s" % (k, other_cached_config[k])
                            self.app.config[k] = other_cached_config[k]

        except:
            import traceback; traceback.print_exc();
            if creating:
                self.destroy()
            raise

    def destroy(self):
        self.save(self.stack.deploy_output_key, "")
        try:
            app = self.heroku.apps[self.stack.url_name]
            code_dir = self.get_code_dir()
            if os.path.exists(code_dir):
                shutil.rmtree(code_dir)
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
        return new_stack
   
    def deploy(self, stack, branch=None, code_only=False, force=False):
        if branch:
            stack.branch = branch

        config = stack.branch.deploy_config
        stack.deploy(config, code_only=code_only, force=force)

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
            if s.id == stack_name or s.url_name == stack_name or s.name == stack_name:
                return s
        
        # Really loose match
        stack_name = stack_name.lower()
        for stack_id, s in self.stacks.items():
            if s.id.lower() == stack_name or s.url_name.lower() == stack_name or s.id.lower() == stack_name or s.name.lower() == stack_name:
                return s

        return None

    def get_stack_from_branch_name(self, branch_name):
        for s_id, s in self.stacks.items():
            if s.branch.name == branch_name or s.branch.name == "feature/%s" % (branch_name,):
                return Stack.restore_from_state(s)
        return None

    def prefixed_name(self, name):
        return "%s%s" % (settings.WILL_DEPLOY_PREFIX, name)
