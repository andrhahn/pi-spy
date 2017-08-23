import ConfigParser

parser = ConfigParser.SafeConfigParser()
parser.read('../../app_config')


def get(key):
    return parser.get('default', key)
