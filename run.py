import logging
from os import environ
from app.application import create_app

logger = logging.getLogger()

MANDATORY_FLASK_VARIABLES = ["FLASK_APP", "SECRET_KEY"]
mandatory_app_variables = MANDATORY_FLASK_VARIABLES

if environ.get('FLASK_DEBUG', 0) == '1':
    logger.info('Running in DEBUG mode')
    environ['FLASK_APP'] = 'kandula-test'
    environ['SECRET_KEY'] = 'kandula-test'
    environ['PYTHONUNBUFFERED'] = '1'

app = create_app()


def validate_mandatory_env_variables():
    for variable in mandatory_app_variables:
        if environ.get(variable) is None:
            raise SystemExit(
                "ERROR: Kandula app must have a valid environment variable of {}. Exiting...".format(variable))


if __name__ == "__main__":
    validate_mandatory_env_variables()
    app.run(host='0.0.0.0', use_evalex=False)
