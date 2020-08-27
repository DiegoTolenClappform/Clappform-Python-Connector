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
The ReadOne() function returns a JSON object with the requested app. It's id needs to have been passed to the class in order to read the app. An exception will be raised upon not finding the app. Additionally the extended parameter can be passed (defaulting to False) in order to expand the data of the collections in the app.

```python
Clappform.App("test_app").ReadOne(extended=True)
```

### Create
The Create() function returns an instance of the App class containing the correct id if the app has been created, otherwise it will raise an exception. For instance an exception will be thrown if the app already exists. The required parameters are: id (Unique, lowercase and seperation by underscores), name, description and icon (ex. "home-icon").

```python
Clappform.App.Create(id="test_app", name="Test App", description="This app gives ... insights on ... subject.", icon="home-icon")
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
The ReadOne() function returns a JSON object with the requested collection. It's slug needs to have been passed to the class in order to read the collection. An exception will be raised upon not finding the collection. Additionally the extended parameter can be passed (defaulting to False) in order to expand the data of the items in the collection.

```python
Clappform.App("test_app").Collection("test_collection").ReadOne(extended=True)
```

### Create
The Create() function returns an instance of the Collection class containing the correct slug if the collection has been created, otherwise it will raise an exception. For instance an exception will be thrown if the collection already exists. The required parameters are: id (Unique, lowercase and separation by underscores), name, description and encryption (Boolean, preferably off for performance but must be on if it will contain personal data).

```python
Clappform.App("test_app").Collection().Create(slug="test_collection", name="Test Collection", encryption=True)
```

### Update
The Update() function returns an instance of the Collection class containing the correct slug if the collection has been updated successfully, otherwise it will raise an exception. For instance an exception will be thrown if the collection couldn't be found. The collection's slug needs to have been passed to the class in order to update the collection. The optional parameters are: name, description and encryption (Boolean)).

```python
Clappform.App("test_app").Collection("test_collection").Create(name="Collection")
```

### Delete
The Delete() function returns True upon successful deletion and raises an exception otherwise. For instance an exception will be thrown if the collection couldn't be found. The collection's slug needs to have been passed to the class in order to delete the collection.

```python
Clappform.App("test_app").Collection("test_collection").Delete()
```

### Empty
The Empty() function returns True upon successful emptying the collection and raises an exception otherwise. The collection's slug needs to have been passed to the class in order to empty the collection.

```python
Clappform.App("test_app").Collection("test_collection").Empty()
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
The ReadOne() function returns a JSON object with the requested item. It's id needs to have been passed to the class in order to read the item. An exception will be raised upon not finding the item.

```python
Clappform.App("test_app").Collection("test_collection").Item("test_item").ReadOne()
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
The Read() function returns a pandas dataframe with all the data stored in the collection. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe.

```python
Clappform.App("test_app").Collection("test_collection").DataFrame().Read()
```

### Synchronize
The Synchronize() function returns True if the dataframe has been synchronized with the collection successfully. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe. The collection will **only** contain the data from the dataframe. The maximum json size to be send is **5MB**, use the Append() method as an alternative. The only parameter is: 'dataframe' and is required to have a pandas dataframe.

```python
Clappform.App("test_app").Collection("test_collection").DataFrame().Synchronize(dataframe=df)
```

### Append
The Append() function returns True if all the data has been added to the collection successfully. The collection's slug needs to have been passed to the collection class in order to retrieve the dataframe. The collection will **only** add the data from the dataframe. The maximum json size to be send is **5MB**, use the Append() method as an alternative. The only parameter is: 'dataframe' and is required to have a pandas dataframe.

```python
Clappform.App("test_app").Collection("test_collection").DataFrame().Append(dataframe=df)
```

## Task
### Read
The Read() function returns an JSON array with all the tasks known to this Clappform instance. Additionally the extended parameter can be passed (defaulting to False) in order to expand the data of the users related to the task.

```python
Clappform.Task.Read(extended=True)
```

### ReadOne
The ReadOne() function returns a JSON object with the requested task. It's id needs to have been passed to the class in order to read the task. An exception will be raised upon not finding the task. Additionally the extended parameter can be passed (defaulting to False) in order to expand the data of the user related to the task.

```python
Clappform.Task(1).ReadOne(extended=True)
```

### Create
The Create() function returns an instance of the Task class containing the correct id if the task has been created, otherwise it will raise an exception. For instance an exception will be thrown if the value types are wrong. The required parameters are: user, name and description. Optional parameters are: due_date (String), completed (Boolean, default: False), archived (Boolean, default: False).

```python
Clappform.Task.Create(user='test@clappform.com', name='Validate the data', description='The data needs to be validated before it gets updated.')
```

### Update
The Update() function returns an instance of the Task class containing the correct id if the task has been updated, otherwise it will raise an exception. For instance an exception will be thrown if the value types are wrong. Optional parameters are: user, name, description, due_date (String), completed (Boolean, default: False), archived (Boolean, default: False).

```python
Clappform.Task(1).Update(completed=True)
```

### Delete
The Delete() function returns True upon successful deletion and raises an exception otherwise. For instance an exception will be thrown if the task couldn't be found. The task's id needs to have been passed to the class in order to delete the task.

```python
Clappform.Task(1).Delete()
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

```python
Clappform.Email.Create(user='test@clappform.com', subject='Data Updated', content='Dear ..., The data has been updated.')
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

## Settings
The settings class is used as module-wide storage for the module. It holds the current token and the base URL.