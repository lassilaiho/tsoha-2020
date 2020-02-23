# Installation
The app supports Python 3.6 and later versions.

[Pipenv](https://pipenv.kennethreitz.org/en/latest/) is used for dependency
management. Make sure it is installed before continuing.

Clone the repository. Install dependencies by running
```
pipenv sync
```
at the root of the repository. To start the app, run
```
pipenv run ./run.py
```

## Configuration
The following settings can be configured:
- debug_mode: boolean (default: false)
  - Configures the app for development, enabling automatic restart on file
    changes, detailed error pages etc.
- database_url: string (default: sqlite:///:memory:)
  - Database connection URL. The app supports PostgreSQL and SQLite databases.
    By default an in-memory SQLite database is used.
- port: integer (default: 5000)
  - The port the server binds to.

The configuration can be provided in the following ways:

### Configuration file
If the environment variable `RECIPE_BOOK_CONFIG` is set to a non-empty value,
the app reads a YAML formatted configuration file from the path specified by the
variable. Settings are specified at the top-level of the YAML document. Omitted
settings are set to their default values.

A sample configuration file
```yaml
debug_mode: false
database_url: sqlite:///recipe-book.db
port: 5000
```

### Environment variables
The app reads configuration variables from environment variables. The variables
are upper-case variants of the configuration variables. For example, to enable
`debug_mode`, set the environment variable `DEBUG_MODE` to `true`. Omitted
settings are set to their default values. Settings from a configuration file
take precedence over settings read from environment variables.

## Deployment
In addition to manually installing the app on a server by following the
instructions above, you can deploy the app using Heroku or Docker.

### Heroku
The project includes a `Procfile` for use in Heroku. Configuration can be
provided using environment variables as explained earlier. Set the environment
variables as Heroku config vars.

Make sure you have the Heroku CLI installed and are logged in.

Create a Heroku app by running
```
heroku create <app name>
```
Add the PostgreSQL addon.
```
heroku addons:create heroku-postgresql
```
The configuration setting `database_url` is automatically set by the PostgreSQL
addon. You may also want to change the port the app listens to. To do so, run
```
heroku config:set PORT=<port number>
```
To deploy the current version of the application, run
```
git push heroku master
```

### Docker
The app supports deployment using Docker. You can build an image using the
Dockerfile provided in the repository, or use a pre-built image tagged
`lassilaiho/recipe-book:latest` from Docker Hub. Configuration for the app can
be provided using environment variables or by bind mounting a configuration file
into the container and setting the environment variable `RECIPE_BOOK_CONFIG` to
point to the mounted configuration file.
