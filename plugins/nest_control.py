from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings
from nest import Nest


class NestPlugin(WillPlugin):

    @respond_to("set the (?:house|heat|temp|temperature) to (?P<temp>.*)")
    def set_the_temp(self, message, temp):
        print "setting %s" % temp
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


    # @respond_to("^what's the house like?")
    # def get_the_temp(self, message, temp):
    #     nest = Nest(
    #         username=settings.NEST_USERNAME,
    #         password=settings.NEST_PASSWORD,
    #         serial=settings.NEST_SERIAL,
    #         units="F",
    #     )
    #     nest.set_temperature(temp)
    #     self.reply(message, "Set the temp to %sF" % temp)


