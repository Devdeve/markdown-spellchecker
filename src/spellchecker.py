#!/usr/bin/env python2

"""This is the main file for the markdown spellcheckers."""
import glob
import os
import enchant
import os.path
import configparser
import json
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
import sys
import argparse
from funct import filechecker
from funct import linechecker
DIRECTORY_TESTS = os.path.dirname(os.path.realpath(__file__))
CONFIGFILE = configparser.ConfigParser()
CONFIGFILECOMPLETEPATH = os.path.join(DIRECTORY_TESTS, 'config.ini')
CONFIGFILE.read(CONFIGFILECOMPLETEPATH)
CONFIGFILE.read(DIRECTORY_TESTS, 'config.ini')
DEFAULTCONFIGFILE = CONFIGFILE['DEFAULT']
DIRECTORY_ROOT = os.path.dirname(DIRECTORY_TESTS)
FILENAME_JSONSCORE = DEFAULTCONFIGFILE['Prevscore']
FILENAME_PWL = DEFAULTCONFIGFILE['PWL']
if not os.path.isabs(FILENAME_JSONSCORE):
    FILENAME_JSONSCORE = os.path.join(
        DIRECTORY_TESTS, DEFAULTCONFIGFILE['Prevscore'])
if not os.path.isabs(FILENAME_PWL):
    FILENAME_PWL = os.path.join(DIRECTORY_TESTS, DEFAULTCONFIGFILE['PWL'])

#print()
if os.path.exists(FILENAME_PWL):
    print("\033[1;36mPWL file exists\033[0m")
    pwl = enchant.request_pwl_dict(FILENAME_PWL)
    #print("Loaded PWL object: %s" % pwl)
    #print("Methods of object: %s" % dir(pwl))
else:
    print("\033[1;36mPWL file does not exist\033[0m")
    sys.exit(2)
# add words to the dictionary used to test for spelling errors
spellcheck = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
wordswrong = open(CONFIGFILE['DEFAULT']['Wordswrongfile'], "w+")
# creates/opens a file to save the words that were spelt wrong
filecheck = open(CONFIGFILE['DEFAULT']['Filecheck'], "w+")
# creates/opens a file to save the files that were checked


def main():
    parser = argparse.ArgumentParser(
        description='Processes Markdown documents for spellchecking')
    parser.add_argument('paths', metavar='PATH', type=str,
                        nargs='*', help='Paths of files to check.')
    args = parser.parse_args()
    if not args.paths:
        print("\033[1;31mInvalid directory or no files exist in said directory or no directory given\033[0m")
        sys.exit(2)
    errortotalprev = 0
    #filechecker(DIRECTORY_POSTS)
    #if os.path.exists(FILENAME_JSONSCORE):
    #    with open(FILENAME_JSONSCORE, 'r') as scorefile:
    #        errortotalprev = json.load(scorefile)
    passed = linechecker(errortotalprev, pwl, args.paths,
                         filecheck, wordswrong, spellcheck, FILENAME_JSONSCORE)
    filecheck.close()
    wordswrong.close()
    if not passed:
        sys.exit(1)


if '__main__' == '__main__':
    main()
