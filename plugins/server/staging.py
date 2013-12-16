import datetime
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
# from plugins.mixins.servers import ServersMixin

class StagingPlugin(WillPlugin,): # ServersMixin

    @respond_to("what branches are available for staging?")
    def available_branches(self, message):
        context = {}
        branches_html = rendered_template("available_branches.html", context)
        self.say(branches_html, message=message, html=True)
    
    @respond_to("what staging stacks (?:do we have|are there)\?")
    def active_staging_servers(self, message):
        context = {}
        branches_html = rendered_template("active_staging_servers.html", context)
        self.say(branches_html, message=message, html=True)
    
    @respond_to("make a new staging stack for (?P<branch_name>\w*)")
    def start_staging(self, message, branch_name=None):
        if not branch_name:
            self.say("You didn't say which branch to stage.")
        else:
            context = {}
            servers_html = rendered_template("active_staging_servers.html", context)
            self.say(servers_html, message=message, html=True)
    
    @respond_to("destroy staging stack (?P<server_name>\w*)")
    def destroy_staging(self, message, server_name=None):
        if not server_name:
            self.say("You didn't say which branch to stage.")
        else:
            context = {}
            servers_html = rendered_template("active_staging_servers.html", context)
            self.say(servers_html, message=message, html=True)
    
    @periodic(hour='17', minute='0', day_of_week="mon-fri")
    def remind_staging_servers(self):
        servers_html = rendered_template("active_staging_server_reminder.html", context)
        self.say(servers_html, message=message, html=True)
