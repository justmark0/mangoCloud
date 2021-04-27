# mangoCloud is cloud storing system
### What you can do using mangoCloud:
- Store your files
- Delete you files
- Share your filet to other users
- Preview images
- Download you files

## How to run it
1. Clone this reposityry to computer and go to its folder
2. If database does not exist ```mangoCloud/db.sqlite3``` you need to create it.
    a. Install requirements.txt using ```pip install -r requirements.txt``` 
    b. Run the server for a few seconds so it creates the database using ```python mangocloud/manage.py runserver```
3. Now you can run it in two ways:
    a. Using docker-compose: ```docker-compose up```
    b. Or using python interpreter (make sure to install the requirements.txt): ```python mangocloud/manage.py runserver```

### Stack of the project:
- Django framework
- JS 