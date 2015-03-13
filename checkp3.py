# -*- coding: utf-8 -*-

import tarfile
import re
import argparse
import gzip
import os.path

ERROR_INCORRECT_FILENAME = 'ERROR: the filename is not correct. The filename must be ID1[_ID2].tar.gz'
ERROR_SPURIOUS_FILE = 'ERROR: file %s does not belong to the list of files of Practice 3'
ERROR_MISSING_FILE = 'ERROR: file %s is missing'
ERROR_P3DATA_CONTENTS = 'ERROR: the contents of P3Data does not follow the required format'
ERROR_MISSING_NAME_OF_STUDENT2 = 'ERROR: the name of the second student is missing from P3Data file'
ERROR_MISSING_ID_OF_STUDENT2 = 'ERROR: the ID of the second student is missing from the name of the compressed file'
ERROR_FILE_ACCESS = 'ERROR: error when reading compressed file %s'

FILENAME = r'^(?P<student1_id>[a-zA-Z0-9]+)(\_(?P<student2_id>[a-zA-Z0-9]+))?.tar.gz$'

REQUIRED_FILES = ['prac3',
                  'prac3/lib',
                  'prac3/free_args.h',
                  'prac3/free_args.c',
                  'prac3/minishell.c',
                  'prac3/minishell_input.h',
                  'prac3/minishell_input.c',
                  'prac3/execute.h',
                  'prac3/execute.c',
                  'prac3/parser.h',
                  'prac3/internals.h',
                  'prac3/jobs.h',
                  'prac3/Makefile',
                  'prac3/P3Data']

P3DATA = r'^STUDENT1=(?P<student1_name>[\w ]+)\s*' + \
         r'STUDENT2=(?P<student2_name>[\w ]+)?\s*' + \
         r'LAST_STEP_TO_BE_GRADED=(?P<last_step>[0-6])\s*\Z'

LIBSHELL_PLATFORMS = ['Darwin/x86_64']


class CheckException(Exception):
    pass


def check_filename(name):
    if name is None:
        return None
    return re.search(FILENAME, name, re.UNICODE)


def check_open_tarfile(fileobj):

    try:
        opened_tarfile = tarfile.open("r:gz", fileobj=fileobj)
    except Exception as error:
        raise CheckException(ERROR_FILE_ACCESS % str(error))

    if not isinstance(opened_tarfile.fileobj, gzip.GzipFile):
        raise CheckException(ERROR_FILE_ACCESS % 'the file is not compressed with gzip')

    return opened_tarfile


def check_files(filetar):

    required_files = REQUIRED_FILES + list(libraries())

    for name in filenames(filetar):
        if name not in required_files:
            raise CheckException(ERROR_SPURIOUS_FILE % name)

    for name in required_files:
        if name not in filenames(filetar):
            raise CheckException(ERROR_MISSING_FILE % name)


def check_p3data_contents(contenido, members):

    p3data_parsed = re.search(P3DATA, contenido, re.MULTILINE | re.UNICODE)

    if p3data_parsed is None:
        raise CheckException(ERROR_P3DATA_CONTENTS)

    p3data_members = p3data_parsed.groupdict()

    if ('student2_id' in members and members['student2_id'] is not None) and \
            ('student2_name' not in p3data_members or p3data_members['student2_name'] is None):
        raise CheckException(ERROR_MISSING_NAME_OF_STUDENT2)

    elif ('student2_id' not in members or members['student2_id'] is None) and \
            ('student2_name' in p3data_members and p3data_members['student2_name'] is not None):
        raise CheckException(ERROR_MISSING_ID_OF_STUDENT2)


def check_p3data(filetar, members):

    try:
        datosp3 = filetar.extractfile('prac3/P3Data')
    except Exception as error:
        raise CheckException(ERROR_FILE_ACCESS % str(error))

    # We have to check that the name of the file matches the contents of P3Data

    try:
        p3data_contents = datosp3.read()
    except Exception as error:
        raise CheckException(ERROR_FILE_ACCESS % str(error))

    check_p3data_contents(p3data_contents, members)


def filenames(members):
    for tarinfo in members:
        yield tarinfo.name


def libraries():
    for plt in LIBSHELL_PLATFORMS:
        d = re.search(r'^(?P<os>\w+)\/(?P<arch>\w+)$', plt).groupdict()

        yield 'prac3/lib/' + d['os']
        yield 'prac3/lib/' + d['os'] + '/' + d['arch']
        yield 'prac3/lib/' + d['os'] + '/' + d['arch'] + '/libshell.a'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('prac3', metavar='FILE', type=file,
                        help='name of the file that contains the files of Practice 3')

    args = parser.parse_args()

    prac3 = args.prac3

    # Filename check

    filename_parsed = check_filename(os.path.basename(prac3.name))

    if filename_parsed is None:
        print(ERROR_INCORRECT_FILENAME)
        exit(-1)

    filename_members = filename_parsed.groupdict()

    # Check the included files

    tar = None

    try:
        tar = check_open_tarfile(prac3)
    except CheckException as e:
        print(str(e))
        exit(-1)

    try:
        check_files(tar)
    except CheckException as e:
        print(str(e))
        exit(-1)

    # Check the contents of P3Data

    try:
        check_p3data(tar, filename_members)
    except CheckException as e:
        print(str(e))
        exit(-1)

    print('OK')
    exit(0)
