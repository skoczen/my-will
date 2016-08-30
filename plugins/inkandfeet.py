import requests
import woopra
from will import settings
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class InkandFeetPlugin(WillPlugin):

    def update_unsubscribes_in_woopra(self, message=None, verbose=False):
        page = 1
        total_pages = 99999999
        while page < total_pages:
            resp = requests.get("https://api.convertkit.com/v3/subscribers?api_secret=%s&page=%s&sort_field=cancelled_at" % (
                settings.CONVERTKIT_SECRET,
                page,
            ))
            skip = False
            try:
                resp.json()["subscribers"]
            except:
                print(resp.content)
                try:

                    # CK is less than reliable.
                    resp = requests.get("https://api.convertkit.com/v3/subscribers?api_secret=%s&page=%s&sort_field=cancelled_at" % (
                        settings.CONVERTKIT_SECRET,
                        page,
                    ))
                except:
                    skip = True
                    self.say("Skipping page %s.  Thanks, Convertkit. :/" % page)

            if not skip:
                for u in resp.json()["subscribers"]:
                    print u["state"]
                    if u["state"] != "active":
                        # Check with woopra, mark unsubscribed if not marked.
                        email = u["email_address"]

                        woopra_resp = requests.get(
                            'https://www.woopra.com/rest/2.4/profile?website=inkandfeet.com&email=%s' % email,
                            auth=(settings.WOOPRA_APP_ID, settings.WOOPRA_KEY),
                        )
                        profile = woopra_resp.json()
                        if "unsubscribed" not in profile["summary"]:
                            # Send unsubscribed event to woopra
                            woopra.identify(woopra.WoopraTracker.EMAIL, email)
                            woopra.track("unsubscribe", {
                                "state": u["state"],
                            })
                            if verbose:
                                print("%s marked as %s" % (email, u["state"]))
                total_pages = int(resp.json()["total_pages"])
                if verbose:
                    print("Page %s of %s" % (page, total_pages))
            page += 1

    @periodic(minute='0', hour='*')
    def hourly_update_unsubscribes_in_woopra(self, message):
        self.update_unsubscribes_in_woopra(message=message)

    @hear("(can you)? check( the)? unsubscribes")
    def hear_update_unsubscribes_in_woopra(self, message):
        self.say("Sure thing.  Give me a minute...", message=message)
        self.update_unsubscribes_in_woopra(message=message, verbose=True)
        self.say("all done!", message=message)
