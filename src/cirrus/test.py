'''
_test_

Command to run available test suites in a package
'''
import os
import posixpath
import sys
from fabric.operations import local

from cirrus.configuration import load_configuration


def main():
    """
    _main_

    Execute test command
    """
    config = load_configuration()

    if len(sys.argv) > 2 and sys.argv[1] != '--suite':
        exit(1)  # only '--suite' is allowed as an option
    elif len(sys.argv) > 2:  # suite has been specified
        local('. ./{0}/bin/activate && nosetests -w {1}'.format(
            config.venv_name(),
            config.test_where(sys.argv[2])))
    else:  # use default
        local('. ./{0}/bin/activate && nosetests -w {1}'.format(
            config.venv_name(),
            config.test_where()))

if __name__ == '__main__':
    main()
