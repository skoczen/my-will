import datetime
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class TimeTopicPlugin(WillPlugin):

    # Disabled for now.
    # @periodic(minute='0')
    def set_topic_time(self):
        now_pst = datetime.datetime.now()
        now_bcn = now_pst + datetime.timedelta(hours=9)

        topic = "PST: %s, Paris: %s" % (now_pst.strftime("%a %I:%M %p"), now_bcn.strftime("%a %I:%M %p"))
        self.set_topic(topic)

    @respond_to("^time$")
    def tell_times(self, message):
        now_pst = datetime.datetime.now()
        now_bcn = now_pst + datetime.timedelta(hours=9)
 
        topic = "PST: %s, Paris: %s" % (now_pst.strftime("%a %I:%M %p"), now_bcn.strftime("%a %I:%M %p"))
        self.reply(message, topic)