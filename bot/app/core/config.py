import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

MONGO_USER = os.getenv('MONGO_ROOT_USER')
MONGO_PASS = os.getenv('MONGO_ROOT_PASS')
MONGO_PORT = os.getenv('MONGO_PORT')

MONGO_URL = f'mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:{MONGO_PORT}/'

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_URL = f'redis://redis:{REDIS_PORT}/0'

MONGO_DATABASE_NAME = 'study_helper'
