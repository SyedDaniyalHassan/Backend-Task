import logging

class PLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Console Handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
