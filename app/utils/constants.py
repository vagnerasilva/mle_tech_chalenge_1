import logging
# Constants
URL = 'https://books.toscrape.com/'
BASE_URL = F'{URL}catalogue/'
API_PREFIX = '/api/v1'


# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance
logger = logging.getLogger(__name__)
