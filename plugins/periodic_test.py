import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings


class RandomTestPlugin(WillPlugin):

    @randomly(start_hour=15, end_hour=18, num_times_per_day=110, day_of_week="fri")
    def random_test(self):
        print "yo" 
