#!/usr/bin/python

import logging
import config_service

log_level = config_service.get_config("log_level")

logging.basicConfig(level = getattr(logging, log_level))

def debug(name, message):
    get_logger(name).debug(message)

def info(name, message):
    get_logger(name).info(message)

def error(name, message):
    get_logger(name).error(message)

def get_logger(name):
    return logging.getLogger(name)
