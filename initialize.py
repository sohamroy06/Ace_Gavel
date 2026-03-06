# Copyright (c) Anish Athalye (me@anishathalye.com)
#
# This software is released under AGPLv3. See the included LICENSE.txt for
# details.

import logging
import time
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('gavel.init')

if __name__ == '__main__':
    # Load .env for local development
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    from gavel import app
    from gavel.models import db

    MAX_RETRIES = 5
    RETRY_DELAY = 3  # seconds

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with app.app_context():
                db.create_all()
                logger.info('Database tables created successfully')
            break
        except Exception as e:
            logger.warning(
                'Database connection attempt %d/%d failed: %s',
                attempt, MAX_RETRIES, str(e)
            )
            if attempt < MAX_RETRIES:
                logger.info('Retrying in %d seconds...', RETRY_DELAY)
                time.sleep(RETRY_DELAY)
            else:
                logger.error('Failed to connect to database after %d attempts', MAX_RETRIES)
                sys.exit(1)
