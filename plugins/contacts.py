from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings

class ContactsPlugin(WillPlugin):

    @respond_to("^set my contact info to (?P<contact_info>.*)", multiline=True)
    def set_my_info(self, message, contact_info=""):
        contacts = self.load("contact_info", {})
        contacts[message.sender.nick] = {
            "info": contact_info,
            "name": message.sender.name,
        }
        self.save("contact_info", contacts)
        self.say("Got it.", message=message)

    @respond_to("^contact info")
    def respond_to_contact_info(self, message):
        contacts = self.load("contact_info", {})
        context = {
            "contacts": contacts,
        }
        contact_html = rendered_template("contact_info.html", context)
        self.say(contact_html)

        
