#!/usr/bin/env python
"""
Git pre-commit tool. Features:
 * Runs code validation scripts;
 * Runs unit-test scripts;
 * Opens a log in the text viewer.
Usage example:
Create a new git pre-commit hook with the following content:
    #!/bin/sh
    c:/python34/python c:/dev/projects/pre-commit-tool/pre-commit.py -vfo -c -t
For more information about parameters, type in the console:
    python pre-commit.py -h
PEP8 validation script can be downloaded here:
https://github.com/PyCQA/pycodestyle/blob/master/pycodestyle.py
"""

__author__ = 'ophermit'

import sys
import argparse
import logging
from os.path import abspath, dirname, join, basename
from subprocess import Popen, PIPE


result_code = 0
def_extension = 'py'
def_exec = sys.executable
def_check = join(dirname(abspath(__file__)), 'pep8.py')
def_test = 'test.py'
def_viewer = 'notepad'

# Setting up argparser
descr = 'Git pre-commit tool. Runs code validation scripts, ' \
        'unit-tests scripts. Opens a log in the text viewer'
parser = argparse.ArgumentParser(description=descr, add_help=True)
parser.add_argument('-v', '--verbose', action='store_true',
                    help='verbose log')
parser.add_argument('-c', '--check', nargs='*',
                    help='list of validation scripts. Each script will be '
                         'work with head revision file list')
parser.add_argument('-t', '--test', nargs='*',
                    help='list of unit-tests scripts')
parser.add_argument('-e', '--exec', default=def_exec,
                    help='executable for run scripts. Current by default')
parser.add_argument('-o', '--openlog', nargs='?', const=def_viewer,
                    help='path to any text viewer')
parser.add_argument('-f', '--forcelog', action='store_true',
                    help='open log even if there are no errors')

params = vars(parser.parse_args(sys.argv[1:]))
if params.get('check') is None and params.get('test') is None:
    print('Pre-commit tool is not properly configured')
    exit(1)

# Set some default values
if params.get('check') is not None and len(params.get('check')) == 0:
    params['check'] = [def_check]
if params.get('test') is not None and len(params.get('test')) == 0:
    params['test'] = [def_test]


# Setting up log
log_filename = 'pre-commit.log'
logging.basicConfig(
    filename=log_filename, filemode='w', format='%(message)s',
    level=logging.INFO)
to_log = logging.info


def shell_command(command, force_report=None):
    """Executes command in the shell
    :param command: Popen args
    :param force_report: reporting about "Popen" results
        True - always
        False - on errors only
        None - never
    :return: tuple (<return code of command>, <console messages of command>)
    """
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    proc.wait()
    transform = lambda x: ' '.join(x.decode('utf-8').split())
    report = [transform(x) for x in proc.stdout]
    report.extend([transform(x) for x in proc.stderr])

    if force_report is True or \
            (force_report is not None and proc.returncode > 0):
        to_log('[ SHELL ] %s (code: %d):\n%s\n'
               % (' '.join(command), proc.returncode, '\n'.join(report)))
    return proc.returncode, report


# Get head revision
code, report = shell_command(
    ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
    params.get('verbose'))
if code != 0:
    result_code = code

targets = filter(lambda x: x.split('.')[-1] == def_extension, report)
targets = [join(dirname(abspath(x)), basename(x)) for x in targets]


# Run validation scripts
if params.get('check') is not None:
    for script in params.get('check'):
        code, report = shell_command(
            [params.get('exec'), script] + targets, params.get('verbose'))
        if code != 0:
            result_code = code


# Run unit-tests
if params.get('test') is not None:
    for script in params.get('test'):
        code, report = shell_command(
            [params.get('exec'), script], params.get('verbose'))
        if code != 0:
            result_code = code


# Open log
if params.get('openlog') and (result_code > 0 or params.get('forcelog')):
    Popen([params.get('openlog'), log_filename], close_fds=True)

print('Result code: %d' % result_code)
exit(result_code)