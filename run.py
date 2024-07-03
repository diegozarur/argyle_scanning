from sys import exit
import os
from typing import Optional

from settings import config_dict, Config
from app import create_app

DEBUG: Optional[str] = os.getenv('DEBUG')

# The configuration
get_config_mode = 'debug' if DEBUG else 'production'

try:
    # Load the configuration using the default values
    app_config: Config = config_dict[get_config_mode.lower()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

flask_app = create_app(app_config)
# Initialize Celery app
celery_app = flask_app.extensions.get("celery")

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=Config.FLASK_PORT)
