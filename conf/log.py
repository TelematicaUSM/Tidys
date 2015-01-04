import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)

fileHandler = logging.FileHandler('log.log')
fileHandler.setLevel(logging.DEBUG)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
