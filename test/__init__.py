from .context import Clappform
from .settings import settings

#These are global vars and need to be filled in when you want to test the package. Then also need to be removed when pushing to git
settings
settings.baseURL = "http://localhost/"
settings.password = ""
settings.username = ""

##### TO-DO #####
# Auth Needs to be made
# File Needs to be made
# Item Needs to be made
# Transfer Needs to be made
# User Needs to be made

# Delete items from dateframe module needs test but not sure how to use function
# Need to look at append and sync functions from dataframe getting error: AttributeError: 'str' object has no attribute 'copy'