import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Clappform

##### NOTES #####

# All test functions MUST start with test. otherwise unittesting does not use them.
# Unittesting works on alphabetical order with its functions and order.

##### END OF NOTES #####

# Testing if we can us globals.
# class Context:
#     def init():
#         global test_url = "http://localhost/"
#         global username = ""
#         global password = ""
#         global app_id = "test_app"
#         global app_name = "Test App"
#         global app_desc = "This app gives ... insights on ... subject."
#         global app_icon = "home-icon"
#         global collection_id = "test_collection"
#         global collection_name = "Test Collection"
#         global collection_desc = "This app gives ... insights on ... subject."
#         global collection_encryption = True
#         global collection_logging = True
#         global collection_sources = []
#         global collection_updated_name = "test case update"
#         global created_collection = ""
#         global updated_collection = ""
#         global deleted_collection = ""
