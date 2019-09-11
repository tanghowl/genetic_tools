import logging

logging.basicConfig(
    level="INFO",
    format="%(asctime)s UpQcInfo %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)
