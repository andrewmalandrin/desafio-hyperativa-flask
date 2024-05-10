import logging
import sys
from app.app import app


if __name__ == "__main__":
    try:
        stream_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler(filename='app_log.log')
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[stream_handler, file_handler],
            format="[%(asctime)s] (%(filename)s:%(lineno)d) %(levelname)s - %(message)s"
        )
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception:
        logging.error("Internal Application Error")
