#Logging files will done by this module.

import logging
import os
from config import BASE_DIR

LOG_FOLDER = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_FOLDER, "app.log")

# create logs folder automatically
os.makedirs(LOG_FOLDER, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)