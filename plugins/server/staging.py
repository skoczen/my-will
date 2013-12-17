import datetime
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from plugins.server.mixins import ServersMixin, GithubMixin

class StagingPlugin(WillPlugin, ServersMixin, GithubMixin):

    @respond_to("refresh (?:repo|branch|github) info")
    def refresh_all_info(self, message):
        self.say("Sure. One minute...", message=message)
        self.refresh_all_cached_github_info()
        self.say("All github branch and repo info refreshed.", message=message)

    @respond_to("(?:what branches are available for staging\?|(?:list|show) deployable branches)")
    def available_branches(self, message):
        print "available_branches"
        repos = self.get_github_deployable_repos()
        context = {"repos": repos}
        branches_html = rendered_template("available_branches.html", context)
        self.say(branches_html, message=message, html=True)

    @respond_to("(?:^what branches do we have open\?|^(?:list|show) (?:all )? branches)")
    def all_branches(self, message):
        print "all_branches"
        repos = self.get_github_all_repos()
        context = {"repos": repos}
        branches_html = rendered_template("available_branches.html", context)
        self.say(branches_html, message=message, html=True)

    
    @respond_to("(?:^what staging stacks (?:do we have|are there)\?|^list stacks)")
    def active_staging_stacks(self, message):
        print "active_staging_stacks"
        context = {}
        branches_html = rendered_template("active_staging_stacks.html", context)
        self.say(branches_html, message=message, html=True)
    
    @respond_to("make a new staging stack for (?P<branch_name>[\w-]*)")
    def start_staging(self, message, branch_name=None):
        if not branch_name:
            self.say("You didn't say which branch to stage.", message=message)

        branch = self.get_branch_from_branch_name(branch_name, is_deployable=True)
        if not branch:
            self.say("Can't find a branch named %s" % branch_name, message=message)
        elif type(branch) is type([]):
            branches_text = "\n-%s".join(branch)
            self.say("Found multiple matches. %s" % branches_text, message=message)
        else:
            new_name = self.get_unused_stack_name()
            # self.say("Making a new stack at http://%s.herokuapp.com/" % new_name["url"], message=message) 
            self.say("Good news: I found the branch you want.\nBad news: I don't know how to do that yet.", message=message)
    
    @respond_to("destroy staging stack (?P<server_name>[\w-]*)")
    def destroy_staging(self, message, server_name=None):
        if not server_name:
            self.say("You didn't say which branch to stage.", message=message)
        else:
            context = {}
            # servers_html = rendered_template("active_staging_stacks.html", context)
            self.say("Sorry, I don't know how to do that yet.", message=message)
    
    @periodic(hour='17', minute='0', second='0', day_of_week="mon-fri")
    def remind_staging_servers(self):
        print "remind_staging_servers"
        context = {}
        # servers_html = rendered_template("active_staging_server_reminder.html", context)
        # self.say(servers_html, html=True)
