from logging import (
	basicConfig, getLogger,
	StreamHandler, Formatter,
	DEBUG, INFO
)

webhook_logger = getLogger('webhook')

__format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
__stream = StreamHandler()

__stream.setFormatter(
	Formatter(__format)
)

webhook_logger.addHandler(__stream)

basicConfig(
	filename = 'webhook.log',
	filemode = 'a',
	format = __format,
	level = INFO
)

webhook_logger.info("Starting WebHook")