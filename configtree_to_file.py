import sys
import argparse
from configtree import Client
from os import environ
from configtree.config_parser import PropertiesParser

EMAIL = environ.get('EMAIL', None)
ORGSLUG = environ.get('ORGSLUG', None)
PASSWORD = environ.get('PASSWORD', None)


def main(args):
    # Check required environment variables exists
    email = EMAIL
    orgslug = ORGSLUG
    password = PASSWORD
    config_path = '/config_file'
    if None in (email, orgslug, password):
        print("EMAIL, ORGSLUG, and PASSWORD environment variables are required!")
        exit(1)

    # Handle commandline args
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-a', '--application', help="Application name", required=True)
    argparser.add_argument('-e', '--environment', help="Environment name", required=True)
    argparser.add_argument('-v', '--version', help="Version name", required=False)
    argparser.add_argument('-f', '--file', help="File name to save the configuration", required=True)

    arguments = argparser.parse_args()

    ct = Client(email=email, orgslug=orgslug, password=password)

    auth_response = ct.get_auth_token()

    if 'error' in auth_response:
        print(str(auth_response))
        exit(1)

    config = ct.get_config(application=arguments.application,
                           environment=arguments.environment,
                           version=arguments.version)
    if 'error' in config:
        print(str(config))
        exit(1)

    pp = PropertiesParser(config)
    pp.parse_data()
    write_status = pp.write_file(path=config_path, filename=arguments.file)
    print(str(write_status))


if __name__ == "__main__":
    main(sys.argv[1:])
