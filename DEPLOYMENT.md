# Craft Shack – Deployment Details

[View README.md file.](/README.md)

[View Craft Shack deployed site here.](https://craft-shack-03a82b9c73ae.herokuapp.com/)

## Deployment

## Table of Contents

- [Deployment Procedure](#deployment-procedure)
- [How to Clone the Repository](#how-to-clone-the-repository)
- [How to Fork the Repository](#how-to-fork-the-repository)

****

## Deployment Procedure

Craft Shack is a Django v5.2.15 project which is using Cloudinary for staticfiles and storage of media and is fully working in the development and is now ready to be deployed to production on Heroku.

### 1. Create an external database with PostgreSQL from Code Institute 

- As a student at Code Institute I created my PostreSQL database with them by submitting my student email address and them sending me the database instance. But you may need to investigate either installing PostreSQL onto your own computer or having it with another company who will host the database for you.

### 2. Create and set up a Heroku app

- Login in with your Heroku email and password at [Heroku](https://heroku.com) or create an account if needed: 
- In the dashboard, click on `new` button and select `create new app`. 
- Add an `APP_NAME`, then select the location, and then click `create app` button.
- Click on the `Settings` tab and scroll to `Config Vars` then click on `Reveal Config Vars` to retrieve our database URL. 
- Next to the `config var` called ‘DATABASE_URL’ copy the Postgres URL in as a value and click on the `Add` button.
- Click on the `Deploy` tab, set it to connect to GitHub – search for the repository and then click `Connect`. Then click to `Enable Automatic Deploys` - every time you push to `main` it will deploy a new version of this app.

### 3. Connect your external database to your IDE

- In the VSCode, create a new file called `env.py` at the top level directory. This file will store our secret environment variables (make sure the `env.py` is added to the `.gitignore` file). 
- In the env.py, import the os library at the top of the file by typing the following into the file: 

```bash
import os 
```

-	Set up environment variables by typing the following into the file: 

```bash
os.environ.setdefault (
"DATABASE_URL",
("Paste in Heroku DATABASE_URL Link" )
)
```
- In the terminal install `dj_database_url v0.5.0` and `psycopg2` to connect to your external database: 

```bash
pip3 install dj_database_url~=0.5.0 psycopg2
```

- Update you `requirements.txt` file with the newly installed packages:

```bash
pip3 freeze –local > requirements.txt
```

-	At the top of the `settings.py` file, import `dj_database_url` underneath the import for os:

```bash
import os
import dj_database_url 
```

-	In the `settings.py` scroll to the `DATABASES` section and comment out the default database and replace it to use the `DATABASE_URL` environment variable:

```bash
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

- In the terminal, run the `showmigrations` command to confirm you are connected to the external database:

```bash
python3 manage.py showmigrations
```

- If you are connected, you should see a list of all migrations, but none of them are checked off.
- In the terminal run the `migrate` command to migrate your database models to your new database:

```bash
python3 manage.py migrate
```

### 4. Fixtures

- `If you did not use fixtures to populate your database` and manually added all your data through the Django Admin, then we need to transfer the data from VSCode to the external database. 
- `If you did use fixtures to populate your database`, then you can follow this step if you want to be able to transfer one file than the several files that you have for an app, or you can continue onto the next step of `loaddata`.
- To transfer the items of your data on VSCode to the external database, will be using the `dumpdata` command in the terminal. This will create a file of the data into a JSON format, and we will then use the `loaddata` command in the terminal to upload the JSON file to the external database.

`Dumpdata`

- To dump the data, we need to make sure that `VSCode is connected to SQLite3 database`. The quickest way to do this is to temporarily comment out the DATABASE_URL setting in the settings.py and correct any indentation:

```bash
# if "DATABASE_URL" in os.environ:
#    DATABASES = {"default: dj_database_url.parse(os.environ.get("DATABASE_URL"))"}
# else:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
```
- Save the `settings.py` file.
- With VSCode now connected to SQLite3, we can `dump` the data that we need. In the terminal write the following command with the `app_name` and `filename` changed to `e.g. python3 manage.py dumpdata craft_shack > items.json`:

```bash
python3 manage.py dumpdata app_name > filename.json
```
- In the `settings.py` file, uncomment the DATABASE_URL` settings and fix the indentation. Just having the production database in settings will avoid any errors of the data being loaded back to the development database:

```bash
# if "DATABASE_URL" in os.environ:
DATABASES = {"default: dj_database_url.parse(os.environ.get("DATABASE_URL"))"}
# else:
#    DATABASES = {
#        "default": {
#            "ENGINE": "django.db.backends.sqlite3",
#            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
```

- Save the `settings.py` file so that VSCode is connected to the external database. In the terminal run `migrate` to make sure that the latest migrations have been applied to the external database:

```bash
python3 manage.py migrate
```

`Loaddata`

- Please note the order you `loaddata` is very important here, so make sure you `load categories first`, then `load subcategories next` and then `load the products`. Whether you are uploading your individual JSON files or a single items one, run `loaddata` in the terminal:

```bash
python3 manage.py loaddata items.json
```
- If your data was uploaded then you will see this in your terminal:

```bash
Installed 130 object(s) from 1 fixtures
```

- Create a superuser for the new external database:

```bash
python3 manage.py createsuperuser
```
Follow the steps in the terminal to create the superuser username and password.

- To prevent exposing our database when pushing to GitHub uncomment the rest and set it up again as the environment variable, and correct the indentation:

```bash
if "DATABASE_URL" in os.environ:
    DATABASES = {"default: dj_database_url.parse(os.environ.get("DATABASE_URL"))"}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
```

### 5. Deploying to Heroku

- First, we need to install `gunicorn` which will act as our webserver and freeze that to our `requirements.txt` file.

```bash
pip3 install gunicorn
pip3 freeze --local > requirements.txt
```

- Create a `Procfile` (with a capital P) in the root directory to tell Heroku to create a web dyno which will run gunicorn and serve our Django app.

```bash
web: gunicorn craft_shack.wsgi:application
```

- We also need to add the hostname of our Heroku app to `ALLOWED_HOSTS` in our `settings.py` file and add the localhost so that VSCode will work too. Remove `https://` from the `start` of the URL, and the `trailing slash` from the `end` of the URL:

```bash
ALLOWED_HOSTS = [
	‘127.0.0.1’,  # Local preview
	'localhost'  # Listen for stripe webhooks
	‘craft-shack-03a82b9c73ae.herokuapp.com’,  # Heroku application
]

- Temporarily disable `collectstatic` by logging into the Heroku account. In the Heroku app, click on the `Settings` tab and scroll to `Config Vars` then click on `Reveal Config Vars`. Set the key and value and click the `Add` button:

```bash
Key: DISABLE_COLLECTSTATIC
Value: 1
```

- After saving the `settings.py` file, we can now add, commit and push to GitHub and push to Heroku to deploy to Heroku with:

```bash
git add .
git commit -m “Your descriptive git message”
git push
git push Heroku main
``` 

### 6. Generate a SECRET_KEY

- If you have already set up and env.py file for your SECRET_KEY earlier in your project, you can skip ahead, but for security reasons you may want to change the secret key.
- You can go to a service such as https://randomkeygen.com/ to generate secret keys. Click on the regenerate button and copy the value.
- In your Heroku app, click on the `Settings` tab and scroll to `Config Vars` then click on `Reveal Config Vars`.
- Create a new Config Var by adding into the `Key` as: `SECRET_KEY` and for the `Value` paste the newly generated secret key created and click the `Add` button.
- In your `settings.py` file and update the SECRET_KEY value to the following:

```bash
SECRET_KEY = os.environ.get('SECRET_KEY')
```

- At the top of the `settings.py` file type `import env`.
- If you don’t already have an `env.py` file then create it at the root level of your app and add it to `.gitignore` file.
- At the top of the `env.py` file type `import os` and add your newly generated key from Heroku to your `env.py` file:

```bash
os.environ["SECRET_KEY"] = “add your newly generated key”
```

- At the top of the `settings.py` file from the root app and navigate to where it says - `from pathlib import Path`. Directly below this import, add the following code: 

```bash
import os 
import dj_database_url 
from pathlib import Path
if os.path.isfile(‘env.py’): 
      import env 
```

- Just below the `SECRET_KEY` in the `settings.py` file set the `DEBUG` to be True only if there is a variable called development in the `env.py`:

```bash
DEBUG = 'DEVELOPMENT' in os.environ
```

- In the `env.py`, add a new environment variable for DEVELOPMENT and set it to ‘1’:

```bash
os.environ.setdefault(‘DEVELOPMENT', ‘1’)
```

- To ensure that Heroku uses the correct version of Python to work with all the project's dependencies, add a `.python-version` file to the root directory. Inside it, add the following line of code:

```bash
3.12.10
```

- Save the `settings.py` file, add, commit and git push these changes.

### 7. Create a Cloudinary account and link it to the project

- Create a Cloudinary account by visiting the Cloudinary website.
- From your Cloudinary dashboard – scroll to the `API Environment Variable` and copy the link. This link will be used to connect our app to Cloudinary. 
- In VSCode open the `env.py` file and add the following code and paste the Cloudinary API Environment Variable link as the value (removing the ‘CLOUDINARY=’ part from the front of the code: 

```bash
os.environ.setdefault(
"CLOUDINARY_URL",
( "cloudinary:// Paste in link")
)
```

- Copy the edited cloundinary API link and open the Heroku app > Settings > Config Vars > `Reveal Config Vars`.
- Add in a new Config Var key of CLOUDINARY_URL and paste in the API link as the value. Then, select `Add`.

- Add Cloudinary libraries to the project

First, we need to install `cloudinary` and `cloudinary_storage` which will act as storage of images and static files and freeze that to our `requirements.txt` file.

```bash
pip3 install cloudinary django-cloudinary-storage
pip3 freeze --local > requirements.txt
```

- In VSCode, open `settings.py` file from the root app and scroll down to the `INSTALLED_APPS` section and install `cloudinary_storage` and `cloudinary`, such that they are placed in the following order: 

```bash
INSTALLED_APPS = [ 
…, 
'cloudinary_storage', 
'django.contrib.staticfiles', 
'cloudinary', 
…, 
] 
```

### 8. Instruct Django to use Cloudinary to store media and static files for project

- In VSCode, open `settings.py` file from the root app, scroll down to `static files` and below this code, add the following code: 

```bash
STATIC_URL=’static/’ 
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

MEDIA_URL = 'media/' 

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "cloudinary_storage.storage.StaticHashedCloudinaryStorage",
    },
}
```

### 9. Push code to GitHub

- In VSCode terminal, push the changes made so far to GitHub by typing the following into the command line: 

```bash
git add . 
git commit –m “deployment commit” 
git push 
```

- Or in the `source code` type the following:
- In the message line add – Deployment to Heroku.
- Click button to commit message.
- Click button to Sync changes to GitHub.

### 10. Deploying manually through Heroku

- In Heroku app click on the Deploy tab:
- Scroll down to Manual Deploy
- Click – Deploy Branch – button
- Click – View / Open app – button

__Note:__ Before deploying to Heroku – always commit to GitHub then login to Heroku. 

### 11. Setting up Stripe

- Login to Stripe, click on the `Developers` link at the bottom left of the page and then `API Keys`.
- Login to Heroku and go to `Settings` then `Config Vars` and add the keys for STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY as the keys and from Stripe copy the token for the published and secret keys to value as follows:

```bash
Key                 Value
STRIPE_PUBLIC_KEY   pk_test_……. 
STRIPE_SECRET_KEY   sk_test_…….
```

- Now we need to create a new webhook endpoint by clicking on `developers` and choosing `webhooks`.
- Click the `Add Destination` button. Click `Your Account` and click into the `Account Section` and `select all Account events` option. 
- Scroll down to and click into the `Charge Section` and `select all Charge events`option.
- Click into the `Checkout section` and choose the options relevant to your case.
- Scroll down to the `Invoice section` and `select all Invoice` options.
- Scroll down to the `Payment Method section` and `select all Payment Method` options.
- Scroll down to the `Refund section` and `select all Refund` options. Click `Continue`.
- Select `Webhook endpoint` and `Continue`.
-Enter a `Destination Name` by adding the `URL` for our `Heroku app`, followed by `/checkout/wh/` to the `Endpoint URL` field, and `Create Destination`.
- We can now reveal our webhooks signing secret and add that to our `Heroku Config Vars`.

```bash
Key             Value
STRIPE_WH_KEY   whsec_test_……. 
```

### How to Clone the Repository

To run the site locally, you can clone the repository into the code editor of your choice. As the code will be linked to my repository, any pushes you make from your repository will come to me for approval. This was not implemented using Gitpod but from my local computer using VS Code via Git to GitHub.

1. Log in to GitHub and locate the [GitHub Repository](add the github link to the website.git).
2. Click on the green code button above the list of files for the drop-down menu.
3. Select the preferred cloning method of HTTPS, SSH, or GitHub CLI and click on the copy button of the web URL to your clipboard.
4. In your IDE, open Git Bash or Terminal
5. Change the current working directory to the one where you want the cloned directory (using cd).
6. In your IDE Terminal, type `git clone` and paste the copied URL from your clipboard add the github link to the website.git.
7. When you press Enter your local clone has been created.
8. Set up a virtual environment.
9. Install the packages from the requirements.txt file. In the terminal type:

```bash
pip3 install -r requirements.txt
```

10. To then stop using the repository and cut ties with it you type in the terminal:

```bash
git remote rm origin
```

****

### How to Fork the Repository

When you fork a GitHub repository you will make a copy of it, which can be put into your own account, and you can make changes without affecting the original repository.

1. Log into GitHub and locate the GitHub Repository you want to fork.
2. At the top of the repository to the right, under the menu, there is a "Fork" button.
3. You should have a copy of the original repository in your own GitHub account.
