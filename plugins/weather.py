import requests
from will import settings
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class OneThingPlugin(WillPlugin):

    @respond_to("weather")
    def respond_to_weather(self, message):
        r = requests.get("https://api.forecast.io/forecast/%s/45.5794,-122.6830" % settings.FORECAST_IO_API_KEY)
        weather = rendered_template("weather.html", r.json())
        self.reply(message, weather, html=True)
