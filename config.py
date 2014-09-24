# Welcome to Will's settings.
# 
# All of the settings here can also be specified in the environment, and should be for
# keys and the like.  In case of conflict, you will see a warning message, and the 
# value in this file will win.


# ------------------------------------------------------------------------------------
# Required
# ------------------------------------------------------------------------------------



# The list of plugin modules will should load. 
# Will recursively loads all plugins contained in each module.


# This list can contain:
# 
# Built-in core plugins:
# ----------------------
# All built-in modules:     will.plugins
# Built-in modules:         will.plugins.module_name
# Specific plugins:         will.plugins.module_name.plugin
#
# Plugins in your will:
# ----------------------
# All modules:              plugins
# A specific module:        plugins.module_name
# Specific plugins:         plugins.module_name.plugin
# 
# Plugins anywhere else on your PYTHONPATH:
# -----------------------------------------
# All modules:              someapp
# A specific module:        someapp.module_name
# Specific plugins:         someapp.module_name.plugin


# By default, the list below includes all the core will plugins and
# all your project's plugins.  

PLUGINS = [
    # Built-ins
    "will.plugins.admin",
    "will.plugins.chat_room",
    "will.plugins.devops",
    "will.plugins.friendly",
    "will.plugins.help",
    "will.plugins.productivity",
    "will.plugins.web",

    # All plugins in your project.
    "plugins",
]

# Don't load any of the plugins in this list.  Same options as above.
PLUGIN_BLACKLIST = [

]


# ------------------------------------------------------------------------------------
# Potentially Required
# ------------------------------------------------------------------------------------

# If will isn't accessible at localhost, you must set this for his keepalive to work.
# Note no trailing slash.
PUBLIC_URL = "http://steven-will.herokuapp.com"

# Port to bind the web server to (defaults to $PORT, then 80.)
# Set > 1024 to run without elevated permission.
# HTTPSERVER_PORT = "9000"


# ------------------------------------------------------------------------------------
# Optional
# ------------------------------------------------------------------------------------

# The list of rooms will should join.  Default is all rooms.
ROOMS = ['Will and I',]

# The room will will talk to if the trigger is a webhook and he isn't told a specific room. 
# Default is the first of ROOMS.
DEFAULT_ROOM = 'Will and I'


# Fully-qualified folders to look for templates in, beyond the two that 
# are always included: core will's templates folder, and your project's templates folder.
# 
# TEMPLATE_DIRS = [
#   os.path.abspath("other_folder/templates")
# ]

# User handles who are allowed to perform `admin_only` plugins.  Defaults to everyone.
# ADMINS = [
#     "steven",
# ]

# Mailgun config, if you'd like will to send emails.

# DEFAULT_FROM_EMAIL="will@example.com"
# Set in your environment:
# export WILL_MAILGUN_API_KEY="key-12398912329381"
# export WILL_MAILGUN_API_URL="example.com"


# Logging level
# LOGLEVEL = "DEBUG"

HANGOUT_URL = ""
