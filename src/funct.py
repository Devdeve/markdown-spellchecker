import os
import enchant
import codecs
import json
import os.path
import re
import logging
import glob


def filechecker(DIRECTORY_POSTS):
    if os.listdir('.') == []:
        print('Please put Prevscore.json in the location of this file.')
        return
    if os.listdir(DIRECTORY_POSTS) == []:
        print('No .md files to evaluate')
        return


def checkline(line, filename, icodeblock, spellcheck, pwl, wordswrong, linenumber):
    regexhtmldirty = re.compile(r'\<(?!\!--)(.*?)\>')
    regexhtmlclean = re.compile(r'\`.*?\`')
    logger = logging.getLogger('markdown-spellchecker')
    logger.info('now checking file %s', filename)
    error = 0
    skipline = False  # defaults to not skip line
    if line.startswith('```') or line == '---':
        icodeblock = not icodeblock
    if icodeblock:
        skipline = True
    if not icodeblock and not skipline:
        htmldirty = regexhtmldirty.sub('', line)  # strips code between < >
        cleanhtml = regexhtmlclean.sub(
            '', htmldirty)  # strips code between ` `
        spellcheck.set_text(cleanhtml)
        for err in spellcheck:
            logger.debug("'%s' not found in main dictionary", err.word)
            if not pwl.check(err.word):
                error += 1
                wordswrong.write('%s in %s\n' % (err.word, filename))
                print("\033[36m%s:%d :\033[0m \033[1;31m%s\33[0m" % (filename, linenumber, err.word))
    return error


def checkfile(filename, pwl, filecheck, wordswrong, spellcheck):
    error = 0
    icodeblock = False
    linelist = codecs.open(filename, 'r', encoding='UTF-8').readlines()
    for linenumber, line in enumerate(linelist):
        error += checkline(line, filename, icodeblock,
                           spellcheck, pwl, wordswrong, linenumber)
    print("\033[36m"+str(error) + ' errors in total in\033[0m \033[1;35m' + str(filename)+"\033[0m")
    filecheck.write('%d errors in total in %s\n' % (error, filename))
    return error


def linechecker(errortotalprev, pwl, filenameslist, filecheck, wordswrong, spellcheck, FILENAME_JSONSCORE):
    errortotal = 0
    for filename in filenameslist:
        for f in glob.glob(filename):
            errortotal += checkfile(filename, pwl, filecheck,
                                    wordswrong, spellcheck)

    return errortotalfunct(errortotal, errortotalprev, FILENAME_JSONSCORE)


def errortotalfunct(errortotal, errortotalprev, FILENAME_JSONSCORE):
    print('\033[1;33mErrors in total: \033[1;34m' + str(errortotal)+"\033[0m")
    if errortotal <= errortotalprev:
        print('\033[1;32mPass. you scored better or equal to the last check\033[0m')
        with open(FILENAME_JSONSCORE, 'w') as outfile:
            json.dump(errortotal, outfile)
            return True
    else:
        print('\033[1;31mFail. try harder next time\033[0m')
        with open(FILENAME_JSONSCORE, 'w') as outfile:
            # saves errortotal to json file for future use
            json.dump(errortotal, outfile)
            return False
