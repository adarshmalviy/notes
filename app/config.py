import os

from dotenv import dotenv_values, load_dotenv

load_dotenv()

config = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ  # override loaded values with environment variables
}

database_url = config['DATABASE_URL']

JWT_SECRET = "mysecret"
