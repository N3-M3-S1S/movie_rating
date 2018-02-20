#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import requests
import argparse

api_key = "fcbb4e77"  # get your own key and put it here if mine doesn't work


def ask_for_title():
    while True:
        t = input("Enter movie title: ")
        if is_title_valid(t):
            return t
        else:
            report_invalid_title(t)


def ask_for_year():
    while True:
        y = input("Enter movie year (optional): ")
        if len(y) == 0:
            return 0
        elif is_year_valid(y):
            return y
        else:
            report_invalid_year(y)


def is_title_valid(t):
    return len(t) > 0


def is_year_valid(y):
    return y.isdigit() and len(str(y)) == 4


def report_invalid_title(t):
    print("Invalid title %s" % t)


def report_invalid_year(y):
    print("Invalid year %s" % y)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--title", help="Movie's title")
parser.add_argument("-y", "--year", help="Release year. If empty - get movie with the most recent release year")
args = parser.parse_args()

if args.title is not None:
    title = args.title
    if not is_title_valid(title):
        report_invalid_title(title)
        sys.exit(1)
else:
    title = ask_for_title()


if args.year is not None:
    year = args.year
    if not is_year_valid(year):
        report_invalid_year(year)
        sys.exit(1)
else:
    '''
     if title wasn't specified as the argument - user will be asked for it in interactive
     mode, so year should be asked for year in interactive mode as well.
    '''
    if args.title is None:
        year = ask_for_year()
    else:
        year = 0

request_params = dict(
    apikey=api_key,
    t=title)

# if there is no year given OMDB will return movie with most recent release year.
if not year == 0:
    request_params['y'] = year

print("Connecting to OMDB...")

try:
    error_key = "Error"
    ratings_key = "Ratings"
    response_json = requests.get("http://www.omdbapi.com/", request_params).json()
    if error_key in response_json:
        print(response_json[error_key])
    elif ratings_key in response_json:
        title = response_json["Title"]
        release_date = response_json["Released"]
        print("%s (%s)" % (title, release_date))
        ratings = response_json[ratings_key]
        for rating in ratings:
            # reverse elements in list so resource name will be in front of score
            resource_score = list(rating.values())[::-1]
            print(": ".join(resource_score))

except requests.RequestException as error:
    print("Can't connect to OMDB:")
    print(error)
