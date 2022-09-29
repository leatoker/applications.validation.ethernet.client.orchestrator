"""logger utility module"""
import logging
import logging.config


def get_logger_instance(level='', logger_name='defaultLogger'):
    """Creates the logger object"""
    log_obj = LogClass()
    logger = log_obj.get_logger(level=level, logger_name=logger_name)
    return logger


class LogClass:
    """Logger class"""

    def get_logger(self, level='', logger_name='defaultLogger'):
        """returns the logger object"""
        # mention the name of the logger according to the requirement
        # refer logger.conf file for the different loggers configured
        logger = logging.getLogger(logger_name)
        if level != '':
            level = level.strip().lower()
            if level == 'debug':
                logger.setLevel(logging.DEBUG)
            elif level == 'info':
                logger.setLevel(logging.INFO)
            elif level == 'warning':
                logger.setLevel(logging.WARNING)
            elif level == 'error':
                logger.setLevel(logging.ERROR)
            elif level == 'critical':
                logger.setLevel(logging.CRITICAL)

        return logger
