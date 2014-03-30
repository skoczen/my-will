from datetime import datetime
import requests


class SkoczenMixin(object):

    def _weight_with_real_dates(self, weight):
        weight["when"] = datetime.strptime(weight["when"], '%Y-%m-%dT%H:%M:%S')
        return weight

    def todays_one_thing(self):
        r = requests.get("http://stevenskoczen.com/manual/one-thing/")
        return r.json()['one_thing']

    def last_weigh_in(self):
        r = requests.get("http://stevenskoczen.com/manual/weights/")
        return self._weight_with_real_dates(r.json()["weights"][0])
        # {
        #     "weight": "152.3",  # lbs
        #     "fat": "16.0",  # %
        #     "when": "timestamp"
        # }

    def weights(self):
        r = requests.get("http://stevenskoczen.com/manual/weights/")
        weights = r.json()
        weights = [self._weight_with_real_dates(w) for w in weights["weights"]]
        print weights
        return weights
