class Log4j(object):
    """
    Thin wrapper around Spark's JVM logger.

    Usage:
        logger = Log4j(spark)
        logger.info("message")
        logger.warn("message")
        logger.error("message")
    """

    def __init__(self, spark):
        # Pick the right JVM logger package depending on the Spark version:
        #   Spark 3.x → org.apache.log4j          (log4j 1.x)
        #   Spark 4.x → org.apache.logging.log4j  (log4j2)
        jvm = spark._jvm
        try:
            log4j = jvm.org.apache.logging.log4j  # log4j2 (Spark 4.x)
        except Exception:
            log4j = jvm.org.apache.log4j          # log4j 1.x (Spark 3.x)

        self.logger = log4j.LogManager.getLogger("retail_analysis")

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def warn(self, message):
        """Log a warning message."""
        self.logger.warn(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)