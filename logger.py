import logging
import logging.config


class BJLog:

    def __init__(self, conf_file_path):
        self.conf_file_path = conf_file_path

    def create_logger(self, app_name):
        logging.config.fileConfig(self.conf_file_path)

        # create logger
        logger = logging.getLogger(app_name)

        return logger
