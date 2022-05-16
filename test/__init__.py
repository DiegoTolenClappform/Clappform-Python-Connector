from .context import Clappform
from .settings import settings

##### NOTES #####

# All test functions MUST start with test. otherwise unittesting does not use them.
# Unittesting works on alphabetical order with its functions and order.

#These are global vars and need to be filled in when you want to test the package. Then also need to be removed when pushing to git
settings
settings.baseURL = ""
settings.password = ""
settings.username = ""
settings.usertestingpassword = ""
settings.usertestingemail = ""
settings.twilliotemplate = ""

##### TO-DO #####
# File Needs to be made ..Need examples of usage 
# Transfer Needs to be made ..First need to finish new function of deleting generated apps that way i can keep repo clear.

##### BUGS/TESTING BUGS #####
# Actionflow not able to start due to Auth issues on API end

# Need to look at append and sync functions from dataframe getting error: AttributeError: 'str' object has no attribute 'copy'
#For now disabled sync and append tests not able to fix it at this time