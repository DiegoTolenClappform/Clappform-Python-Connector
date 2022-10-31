# Python API Connector
## General Information

This connector is an interface to be used by App Developers to swiftly write (import) scripts in Python in combination with the storing of said data in Clappform.

This connector comes pre-installed on every instance of Clappform and can be imported into a python script with the following command:
```python
import Clappform
```

If you wish to use this connector locally for testing purposes you can install it using:
```bash
pip install Clappform
```

Now the interface is accessible in your code by prefixing with 'Clappform'. The only other method that's in every case needed it the instantiating of the authentication handler which will be described in the next chapter. Additional info can be given programmatically by using Python's help() function on any of this modules classes.

**DISCLAIMER:** *Use this connector wisely and with caution. Always make sure you're working with backups and test data. Otherwise important data or progress can be lost. Usage of the API or altering scripts made by Clappform can lead to losing warranty on your data.*

## Authentication
All authentication is handled by the Auth class. The Auth class is exposed through Clappform and needs to be initiated before any other commands, all authentication afterwards will be handled (including refreshing the token). Three parameters are needed: the base URL of the environment to authenticate towards (ex. https://dev.clappform.com/), the username and the password. The class has more exposed function, but those are only needed for the handler.

```python
Clappform.Auth(baseURL="https://dev.clappform.com/", username="test@clappform.com", password="test")
```

**NOTE:** *It's strongly recommended to create per environment a seperate user for the importing scripts*

# Exposed Classes
In this section all the available functions of the module will be described.

## App
### Read
The Read() function returns an JSON array with all the apps known to this Clappform instance. Additionally the extended parameter can be passed (defaulting to False) in order to expand the data of the collections in the app.

```python
Clappform.App.Read(extended=True)
```

### ReadOne
The ReadOne() function returns a JSON object with the requested app. It's id needs to have been passed to the class in order to read the app. An exception will be raised upon not finding the app. Additionally the extended pa rameter can be passed (defaulting to False) in order to expand the data of the collections in the app.

```python
Clappform.App("test_app").ReadOne(extended=True)
```

### Create
The Create() function returns an instance of the App class containing the correct id if the app has been created, otherwise it will raise an exception. For instance an exception will be thrown if the app already exists. The required parameters are: id (Unique, lowercase and seperation by underscores), name, description and icon (ex. "home-icon").

```python
Clappform.App.Create(id="test_app", name="Test App", description="This app gives ... insights on ... subject.", opts={})
```

### Update
The Update() function returns an instance of the App class containing the correct id if the app has been updated successfully, otherwise it will raise an exception. For instance an exception will be thrown if the app couldn't be found. The app's id needs to have been passed to the class in order to update the app. The optional parameters are: name, description and icon (ex. "home-icon").

```python
Clappform.App("test_app").Update(name="App")
```

### Delete
The Delete() function returns True upon deletion and raises an exception otherwise. For instance an exception will be thrown if the app couldn't be found. The app's id needs to have been passed to the class in order to delete the app.

```python
Clappform.App("test_app").Delete()
```

## Collection
The Collection() function returns an instance of the Collection class. An collection's id can be passed to be able to read, update or delete a specific collection.

```python
Clappform.App("test_app").Collection("test_collection")
```

### Collection
### ReadOne
The ReadOne() function returns a JSON object with the requested collection. It's slug needs to have been passed to the class in order to read the collection. An exception will be raised upon not finding the collection. Additionally an extended level parameter of `0` to `3` (default: `0`) can be passed in order to expand the data of the items in the collection. If the collection is locked, setting the 'original' parameter to equal `False` will show the data after the lock occured.

```python
Clappform.App("test_app").Collection("test_collection").ReadOne(extended=0, original=True)
```

### Create
The Create() function returns an instance of the Collection class containing the correct slug if the collection has been created, otherwise it will raise an exception. For instance an exception will be thrown if the collection already exists. The required parameters are: id (Unique, lowercase and separation by underscores), name, description, encryption (Boolean, preferably off for performance but must be on if it will contain personal data), logging (Boolean, Set to true if the collection needs to be logged in the admin panel, we suggest setting this to true if all changes to the collection needs to be tracked) and sources (list of resources used from where the data in the collection was gathered, defaults to an empty array).

```python
Clappform.App("test_app").Collection().Create(slug="test_collection", name="Test Collection", description="This collection stores data about ... and is used in ...", encryption=True, logging=True, sources=[{ "name": "Online resource", "link": "https://www.example.com/" }, "Name without link"])
```

### Update
The Update() function returns an instance of the Collection class containing the correct slug if the collection has been updated successfully, otherwise it will raise an exception. For instance an exception will be thrown if the collection couldn't be found. The collection's slug needs to have been passed to the class in order to update the collection. The optional parameters are: name, description, encryption (Boolean)), logging (Boolean, Set to true if the collection needs to be logged in the admin panel, we suggest setting this to true if all changes to the collection needs to be tracked) and sources (list of resources used from where the data in the collection was gathered).

```python
Clappform.App("test_app").Collection("test_collection").Update(name="Collection")
```

### Delete
The Delete() function returns True on successful deletion and otherwise throws an exception. For example, an exception will be thrown if the collection could not be found. The slug of the collection must have been passed to the class to delete the collection. If the collection is used by modules, the function returns an error message and two options are available: update the related module or delete it. To update the related modules, specify the parameters 'slug' and 'app'. To delete the related modules, set the 'delete_modules' parameter to True. If neither option is set, the function refuses to delete the collection and returns a list of all modules associated with the collection. In case both update AND delete parameters are passed, the function overrides the delete.

```python
Clappform.App("test_app").Collection("test_collection").Delete()
```
```python
Clappform.App("test_app").Collection("test_collection").Delete(slug="new_collection_slug", app="new_app_id")
```
```python
Clappform.App("test_app").Collection("test_collection").Delete(delete_modules=True)
```
### Empty
The Empty() function returns True upon successful emptying the collection and raises an exception otherwise. The collection's slug needs to have been passed to the class in order to empty the collection.

```python
Clappform.App("test_app").Collection("test_collection").Empty()
```

### Query
The Query() function returns a pandas dataframe with the data matching specified conditions stored in the collection. The options follow the MongoDB documentation. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe. If the collection is locked, setting the 'Original' parameter to equal False will show the data after the lock occured.

```python
Clappform.App("test_app").Collection("test_collection").Query(data_source='foo', query=[], name='Bar', slug='bar ', **kwargs)
```

### Lock
The Lock() function returns True upon success. It duplicates the current collection so one can be read by the user whilst the new one is being worked at. The new data can be read by using the parameter Original and setting it to equal false for the read function being used. The collection's slug needs to have been passed to the class in order to empty the collection.

```python
Clappform.App("test_app").Collection("test_collection").Lock()
```

### Unlock
The Unlock() function True returns upon success. It removes the duplicate created by the Lock() function. After running this function all the changes that have been made to the collection will be served to the users. The collection's slug needs to have been passed to the class in order to empty the collection.

```python
Clappform.App("test_app").Collection("test_collection").Unlock()
```

### Item
The Item() function returns an instance of the Collection class. An item's id can be passed to be able to read, update or delete a specific item. The collection's slug needs to have been passed to the collection class in order to create an instance of an item.

```python
Clappform.App("test_app").Collection("test_collection").item("test_item")
```

### DataFrame
The DataFrame() function returns an instance of the DataFrame class for this collection.

```python
Clappform.App("test_app").Collection("test_collection").DataFrame()
```

## Item
### ReadOne
The ReadOne() function returns a JSON object with the requested item. It's id needs to have been passed to the class in order to read the item. An exception will be raised upon not finding the item. If the collection is locked, setting the 'Original' parameter to equal False will show the data after the lock occured.

```python
Clappform.App("test_app").Collection("test_collection").Item("test_item").ReadOne(Original=True)
```

### Create
The Create() function returns an instance of the Item class containing the correct id if the item has been created, otherwise it will raise an exception. For instance an exception will be thrown if the item already exists. The required parameters are: id (Unique, lowercase and separation by underscores) and data (must be transformable to JSON, for instance an array or an object).

```python
Clappform.App("test_app").Collection("test_collection").Item.Create(id="test_item", data={ "property": "value" })
```

### Update
The Update() function returns an instance of the Item class containing the correct id if the collection has been updated successfully, otherwise it will raise an exception. For instance an exception will be thrown if the item couldn't be found. The item's id needs to have been passed to the class in order to update the item. The required parameter is: "data" (must be transformable to JSON, for instance an array or an object)).

```python
Clappform.App("test_app").Collection("test_collection").Item("test_item").Update(data={ "property": "value" })
```

### Delete
The Delete() function returns True upon successful deletion and raises an exception otherwise. For instance an exception will be thrown if the item couldn't be found. The item's id needs to have been passed to the class in order to delete the item.

```python
Clappform.App("test_app").Collection("test_collection").Item("test_item").Delete()
```

## DataFrame
### Read
The Read() function returns a pandas dataframe with all the data stored in the collection in iterations using yield. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe. If the collection is locked, setting the 'Original' parameter to equal False will show the data after the lock occured.

```python
for data in Clappform.App("test_app").Collection("test_collection").DataFrame().Read(Original=True):
    print(data)
```

### Synchronize
The Synchronize() function returns True if the dataframe has been synchronized with the collection successfully. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe. The collection will **only** contain the data from the dataframe. The maximum json size to be send is **5MB**, use the Append() method as an alternative. The only parameter is: 'dataframe' and is required to have a pandas dataframe.

```python
Clappform.App("test_app").Collection("test_collection").DataFrame().Synchronize(dataframe=df)
```

### Append
The Append() function returns True if all the data has been added to the collection successfully. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe. The collection will **only** add the data from the dataframe. The maximum json size to be send is **5MB**, use the Append() method as an alternative. The only parameter is: 'dataframe' and is required to have a pandas dataframe. The 'show' parameter shows all the changes made to the columnnames. The parameter 'n_jobs' is the amount of threads that will be used.
The dataframe will be altered to make the data more uniform for Clappform, the steps in which it gets altered is:
    <br/> 1. All columnnames will be lowercased
    <br/> 2. multiple spaced will be replaced with a single space for every columnname
    <br/> 3. All '-' and spaces will be replaced with '_' in the columnnames
    <br/> 4. All columnnames will be striped
    <br/> 5. In every columnname characters which are not valid as variable names in Javascript will be removed
    <br/> 6. Every cell will be striped unless it is a List
    <br/> 7. All columnnames will be striped
    <br/> 8. All columnnames which start with a number will lose its first character until it starts with an '_', '$' or letter
<br/><br/>
If the columnname is empty because it doesnt


```python
Clappform.App("test_app").Collection("test_collection").DataFrame().Append(dataframe=df, n_jobs = 1, show = False)
```

### Query
The Query() function returns a pandas dataframe with the data matching specified conditions stored in the collection. The options follow the MongoDB documentation. It is necessary to have all columns (except id) in the data property if changing the projection. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe. If the collection is locked, setting the 'Original' parameter to equal False will show the data after the lock occured.

```python
Clappform.App("test_app").Collection("test_collection").DataFrame().Query(filters={}, projection={},  sorting={}, original=True)
```

## Notification
### Read
The Read() function returns an JSON array with all the notifications known to this Clappform instance.

```python
Clappform.Notification.Read()
```

### ReadOne
The ReadOne() function returns a JSON object with a single notification. It's id needs to have been passed to the class in order to read the notification.

```python
Clappform.Notification(1).ReadOne()
```

### Create
The Create() function returns an instance of the Notification class containing the correct id if the notification has been created, otherwise it will raise an exception. For instance an exception will be thrown if the value types are wrong. The required parameters are: user, content and url (String, relative path to page opened on opening the notification).

```python
Clappform.Notification.Create(user='test@clappform.com', content='Data has been updated', url='/app/test_app')
```

### Update
The Update() function returns an instance of the Notification class containing the correct id if the notification has been updated, otherwise it will raise an exception. For instance an exception will be thrown if the value types are wrong. Optional parameters are: is_opened (Boolean).

```python
Clappform.Notification(1).Update(is_opened=True)
```

### Delete
The Delete() function returns True upon successful deletion and raises an exception otherwise. For instance an exception will be thrown if the notification couldn't be found. The notification's id needs to have been passed to the class in order to delete the notification.

```python
Clappform.Notification(1).Delete()
```

## Email
### Read
The Read() function returns an JSON array with all the emails known to this Clappform instance.

```python
Clappform.Email.Read()
```

### ReadOne
The ReadOne() function returns a JSON object with a single email. It's id needs to have been passed to the class in order to read the email.

```python
Clappform.Email(1).ReadOne()
```

### Create
The Create() function returns an instance of the Email class containing the correct id if the email has been sent, otherwise it will raise an exception. For instance an exception will be thrown if the user couldn't be found. The required parameters are: user, subject and content.

#### Note Currently for internal use only.

```python
Clappform.Email.Create( template_id="id string", tojson={}, templatejson={}, fromjson={})
```

## SMS
### Read
The Read() function returns an JSON array with all the sms messages known to this Clappform instance.

```python
Clappform.SMS.Read()
```

### ReadOne
The ReadOne() function returns a JSON object with a single SMS message. It's id needs to have been passed to the class in order to read the SMS message.

```python
Clappform.SMS(1).ReadOne()
```

### Create
The Create() function returns an instance of the SMS class containing the correct id if the SMS message has been sent, otherwise it will raise an exception. For instance an exception will be thrown if the user couldn't be found. The required parameters are: user and content.

```python
Clappform.SMS.Create(user='test@clappform.com', content='Data has been updated')
```


## Whatsapp
### Read
The Read() function returns an JSON array with all the Whatsapp messsages known to this Clappform instance.

```python
Clappform.Whatsapp.Read()
```

### ReadOne
The ReadOne() function returns a JSON object with a single Whatsapp message. It's id needs to have been passed to the class in order to read the Whatsapp message.

```python
Clappform.Whatsapp(1).ReadOne()
```

### Create
The Create() function returns an instance of the Whatsapp class containing the correct id if the Whatsapp message has been sent, otherwise it will raise an exception. For instance an exception will be thrown if the user couldn't be found. The required parameters are: user and content.

```python
Clappform.Whatsapp.Create(user='test@clappform.com', content='Data has been updated')
```

## Worker
### from_getenv
The `from_getenv()` funtion returns an instance of the Worker class. With this instance one can interact with the Worker cache for a specific actionflow. The `Get(key)`, `Set(key)` and `Keys()` methods are described in further detail in the sections below. By default `from_getenv()` loads its configuration from the `WORKER_TASK_OPTIONS` environment variable, this can be changed setting the `var` keyword argument e.g. `from_getenv(var="EXAMPLE")`. The value of the environment variable must be a JSON string with the following keys: env, action_flow, userid, redis_uri.

The Worker always sets the `WORKER_TASK_OPTIONS` environment variable when executing tasks. When using the `Worker` class one can create an instance as follow:

```python
w = Clappform.Worker.from_getenv()
```

### Get
`Get(key)` Is a method that retrieves the value for that given key. `key` Must be of type `str`. The return value is based on the input given to the `Set()` method.
```python
>>> w.Get("key1")
b'I like turtles!'
```

### Set
The `Set(key, value)` allows for storing key value pairs inside the cache. `key` Must be of type `str` and value must be one of: `bytes`, `memoryview`, `str`, `int` or `float`.
```python
>>> w.Set("key1", "I like turtles!")
```

### Keys
With `keys()` you get a list of known keys.
```
>>> w.Keys()
[b'https://example.clappform.com_1_1_spam', b'https://example.clappform.com_1_1_eggs', b'https://example.clappform.com_1_1_foo']
```


## Settings
The settings class is used as module-wide storage for the module. It holds the current token and the base URL.

## User

### Create
The create function allows you to create a public user when using the authkey. This function is made for internal use only and added to the readme for documentation.

#### Note Currently for internal use only.
only has been added to the readme for documentation.

```python
Clappform.User.Create(clappformuri='https://www.example.com/', authpassword='secret', email='newusermail@mail.com', firstname="firstname", lastname='lastname', phone='+31600000000', password='another secret')
```
