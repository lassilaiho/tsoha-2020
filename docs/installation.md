# Installation
The project uses [Pipenv](https://pipenv.kennethreitz.org/en/latest/) for
dependency management. Make sure it is installed before continuing.

Clone the repository. Install dependencies by running
```
pipenv install
```
at the root of the repository. To start the app, run
```
pipenv run ./run.py
```

## Configuration
The following settings can be configured:
- debug_mode: true|false (default: false)
  - Configures the app for development, enabling automatic restart on file
    changes, detailed error pages etc.
- database_url: string (default: sqlite:///:memory:)
  - Database connection URL. The app uses an in-memory SQLite database by
    default.
- port: integer (default: 5000)
  - The port the server binds to.

The configuration can be provided in the following ways:

### Configuration file
If the environment variable `RECIPE_BOOK_CONFIG` is set to a non-empty value,
the app reads a YAML formatted configuration file from the path specified by the
variable. Settings are specified at the top-level of the YAML document. Omitted
settings are set to their default values.

### Environment variables
If the environment variable `RECIPE_BOOK_CONFIG` is empty or not defined and
`RECIPE_BOOK_CONFIG_ENV` is set to a non-empty value, the app reads the
configuration from environment variables. The variables are upper-case variants
of the configuration settings. For example, to enable `debug_mode`, set the
environment variable `DEBUG_MODE` to `true`. Omitted settings are set to their
default values.

## Heroku
The project includes a `Procfile` for use in Heroku. Configuration can be
provided using environment variables as explained earlier. Set the environment
variables as Heroku config vars. Remember to set `RECIPE_BOOK_CONFIG_ENV` to a
non-empty value.

### Deployment
Make sure you have the Heroku CLI installed.

Create a Heroku app by running
```
heroku create <app name>
```
To deploy the current version of the application, run
```
git push heroku master
```
