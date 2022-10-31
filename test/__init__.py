from .context import Clappform
from .settings import settings

##### NOTES #####

# All test functions MUST start with test. otherwise unittesting does not use them.
# Unittesting works on alphabetical order with its functions and order.

# These are global vars and need to be filled in when you want to test the package. Then also need to be removed when pushing to git
settings
settings.baseURL = "http://localhost/"
settings.password = "Migration12!"
settings.username = "d.tolen@clappform.com"
settings.usertestingpassword = "Migration12!"
settings.usertestingemail = "d.tolen@clappform.com"
settings.twilliotemplate = ""

##### TO-DO #####
# File Needs to be made ..Need examples of usage
# Transfer Needs to be made ..First need to finish new function of deleting generated apps that way i can keep repo clear.

##### BUGS/TESTING BUGS #####
# Appear to be no more known bugs

##### NOTES #####
# Actionflow tests diabled because worker is not connected to localhost
