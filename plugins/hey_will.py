import json
import requests
from will import settings
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class HeyWillPlugin(WillPlugin):

    @route("/hey-will/")
    def hey_will_listener(self):
        try:
            if "phrase" in self.request.params:
                message = self.request.params["phrase"]
                if not "@will" in message:
                    message = "@will %s" % message

                # Total hack.  Should do this properly in will, with an "as" or "token" param.
                context = {
                    "room_id": self.get_room_by_jid(settings.WILL_DEFAULT_ROOM)['room_id'],
                    "token": settings.PERSONAL_HIPCHAT_TOKEN,
                }
                url = "https://api.hipchat.com/v2/room/%(room_id)s/notification?auth_token=%(token)s" % context
                data = {"message": message}
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(url, headers=headers, data=json.dumps(data))
                return "You got it."
            else:
                return "Sorry, couldn't hear you!"
        except:
            return "Sorry, something went wrong!"
