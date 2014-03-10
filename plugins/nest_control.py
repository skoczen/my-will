from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings
from nest import Nest


class NestPlugin(WillPlugin):


    @respond_to("set the (?:house|heat|temp|temperature) to (?P<temp>.*)")
    def set_the_temp(self, message, temp):
        temp = int(temp)
        nest = Nest(
            username=settings.NEST_USERNAME,
            password=settings.NEST_PASSWORD,
            serial=settings.NEST_SERIAL,
            units="F",
        )
        nest.login()
        nest.set_temperature(temp)
        self.reply(message, "Done. I set the temp to %sF." % temp)

    @respond_to("^what's the house like?")
    def get_the_temp(self, message):
        nest = Nest(
            username=settings.NEST_USERNAME,
            password=settings.NEST_PASSWORD,
            serial=settings.NEST_SERIAL,
            units="F",
        )
        nest.login()
        nest.get_status()
        context = {
            "current_temp": nest.temp_out(nest.status['shared'][nest.serial]['current_temperature']),
            "target_temp": nest.temp_out(nest.status['shared'][nest.serial]['target_temperature']),
            "current_humidity": nest.status['device'][nest.serial]['current_humidity'],
            "is_on": nest.status['shared'][nest.serial]['hvac_heater_state'],
        }
        status_text = rendered_template("house_status.html", context)
        self.reply(message, status_text, html=True)
