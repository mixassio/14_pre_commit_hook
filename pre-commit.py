import sys
import argparse
from subprocess import Popen, PIPE


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', nargs='*')

params = vars(parser.parse_args(sys.argv[1:]))

# Set some default values
if params.get('test') is not None and len(params.get('test')) == 0:
    params['test'] = ['tests.py']


def shell_command(command):
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    proc.wait()
    transform = lambda x: ' '.join(x.decode('utf-8').split())
    report = [transform(x) for x in proc.stdout]
    report.extend([transform(x) for x in proc.stderr])
    print('\n'.join(report))
    return proc.returncode, report


# Run unit-tests
result_code = 0
if params.get('test') is not None:
    for script in params.get('test'):
        code, report = shell_command([sys.executable, script])
        if code != 0:
            result_code = code

exit(result_code)