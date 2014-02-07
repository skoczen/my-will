from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings
from plugins.server.mixins.servers import BIGGEST_FISH_NAMES, STACKS_KEY

class CleanAWSBucketsPlugin(WillPlugin):

    def clean_buckets(self, message=None, quiet=True):
        try:
            from boto.s3.connection import S3Connection
            if (self.verify_setting_exists("WILL_AWS_ACCESS_KEY_ID", message=message) and 
                self.verify_setting_exists("WILL_AWS_SECRET_ACCESS_KEY", message=message) and
                self.verify_setting_exists("WILL_AWS_DEV_BUCKET_NAME", message=message)
               ):
                conn = S3Connection(settings.WILL_AWS_ACCESS_KEY_ID, settings.WILL_AWS_SECRET_ACCESS_KEY)

                # 
                buckets_to_clean = [settings.WILL_AWS_DEV_BUCKET_NAME,]
                for fish in BIGGEST_FISH_NAMES:
                    buckets_to_clean.append("%s%s" % (settings.WILL_DEPLOY_PREFIX, fish))

                stacks = self.load(STACKS_KEY, {})
                for name in stacks.keys():
                    prefixed_name = "%s%s" % (settings.WILL_DEPLOY_PREFIX, name)
                    if prefixed_name in buckets_to_clean:
                        buckets_to_clean.remove(prefixed_name)

                num_removed = 0
                if len(buckets_to_clean) > 0:
                    for bucket_name in buckets_to_clean:
                        bucket = None
                        try:
                            bucket = conn.get_bucket(bucket_name)
                        except:
                            pass
                        if bucket:
                            for key in bucket.list():
                                key.delete()
                                num_removed += 1

                if num_removed > 0 or quiet is False:
                    self.say("I just cleaned up the dev buckets on AWS. %s objects deleted." % num_removed, message=message)

        except ImportError:
            self.say("Boto library not installed. Can't clean the dev buckets.", message=message)
            

    @periodic(hour='1', minute='0')
    def clean_buckets_at_1_am(self):
        self.clean_buckets()

    @respond_to("(clear|clean ?up|empty) the dev buckets?")
    def clean_buckets_reply(self, message):
        self.say("Sure thing. Gimme a minute or two.", message=message)
        self.clean_buckets(message=message, quiet=False)