import os
from dotenv import load_dotenv

load_dotenv()

bind = f'0.0.0.0:{os.getenv("FLASK_PORT")}'
workers = 1
accesslog = '-'
loglevel = 'debug'
