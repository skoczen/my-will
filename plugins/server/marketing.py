from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template

class MarketingPlugin(WillPlugin):

    @route("/marketing-deployed/<success_code>")
    def deploy_output(self, success_code):
        if success_code == "0":
            self.say("Marketing site deployed successfully: http://gk-marketing.s3-website-us-east-1.amazonaws.com/")
        else:
            self.say("Error deploying marketing site.", color="red")
        return "Success"

