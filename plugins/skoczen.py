import requests


class SkoczenMixin(object):

    def todays_one_thing():
        r = requests.get("http://stevenskoczen.com/manual/one-thing/")
        return r.json()['one_thing']

    def last_weigh_in():
        r = requests.get("http://stevenskoczen.com/manual/weights/")
        return r.json()["weights"][0]
        # {
        #     "weight": "152.3",  # lbs
        #     "fat": "16.0",  # %
        #     "when": "timestamp"
        # }

    def weights():
        r = requests.get("http://stevenskoczen.com/manual/weights/")
        return r.json()
