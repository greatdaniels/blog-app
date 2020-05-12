# blog-app

## Author

[Dan_Njoroge](https://github.com/greatdaniels)

# Description
This is an application that allows users to view blogs, comment on these blogs, and subscribe to receive an email once a new blog is posted by a writer. It also allows writers to post, edit, and delete blogs.

## User Story

* A user can view the most recent posts.
* View and comment the blog posts on the site.
* A user should an email alert when a new post is made by joining a subscription.
* Register to be allowed to log in to the application
* A user sees random quotes on the site
* A writer can create a blog from the application and update or delete blogs I have created.

## Development Installation
To get the code..

1. Cloning the repository:
  ```bash
  git clone https://github.com/greatdaniels/blog-app.git
  ```
2. Move to the folder and install requirements
  ```bash
  cd blog-app
  pip install -r requirements.txt
  ```
3. Exporting Configurations
  ```bash
  export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://{User Name}:{password}@localhost/{database name}
  ```
4. Running the application
  ```bash
  python3.6 manage.py server
  ```
5. Testing the application
  ```bash
  python3.6 manage.py test
  ```
Open the application on your browser `127.0.0.1:5000`.


## Technology used

* [Python3.6](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Heroku](https://heroku.com)


## Known Bugs
* Pull requests are allowed incase you spot a bug.

## License
[MIT LICENSE](./license)