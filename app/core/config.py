import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

MONGO_USER = os.getenv('MONGO_ROOT_USER')
MONGO_PASS = os.getenv('MONGO_ROOT_PASS')

MONGO_URL = f'mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:27017/'

MONGO_DATABASE_NAME = 'study_helper'
