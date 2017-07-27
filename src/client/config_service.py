import ConfigParser

parser = ConfigParser.SafeConfigParser()
parser.read('../app_config')


def get_config(key):
    return parser.get('default', key)
