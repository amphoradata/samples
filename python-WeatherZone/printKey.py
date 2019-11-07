from weatherzone import generate_key
import argparse

parser = argparse.ArgumentParser(description='Print your WeatherZone key.')

parser.add_argument('password', metavar='P', help='WeatherZone API Password')

args = parser.parse_args()

password = args.password

key = generate_key(password)

print(key)