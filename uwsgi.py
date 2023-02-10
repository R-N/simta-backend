import os
import sys

ROOT_DIR = "a"

try:
    import logging, logging.handlers
    logger = logging.getLogger()

    """
    h = logging.handlers.SysLogHandler(address=("a", 0), facility='user')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(h)
    """

    sys.path.append(ROOT_DIR)
    os.chdir(ROOT_DIR)
    os.environ["LOG_DIR"] = os.path.join(ROOT_DIR, "logs")

    sys.stderr.write = logger.error
    sys.stdout.write = logger.info
except Exception as ex:
    err = ex

from simta import create_app
app = create_app()

if __name__ == '__main__':
    app.run()