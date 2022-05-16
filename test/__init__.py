from .context import Clappform
from .settings import settings

##### NOTES #####

# All test functions MUST start with test. otherwise unittesting does not use them.
# Unittesting works on alphabetical order with its functions and order.

#These are global vars and need to be filled in when you want to test the package. Then also need to be removed when pushing to git
settings
settings.baseURL = "http://localhost/"
settings.password = ""
settings.username = ""
settings.usertestingpassword = ""
settings.usertestingemail = ""

##### TO-DO #####
# File Needs to be made ..Need examples of usage
# Transfer Needs to be made ..Do we need this test as we dont want to fill up github repo with gunk

##### BUGS #####
# Update and Delete are not active in the API routing for notifications
# Actionflow not able to start due to Auth issues on API end
# Need template id for sending email.

# Need to look at append and sync functions from dataframe getting error: AttributeError: 'str' object has no attribute 'copy'