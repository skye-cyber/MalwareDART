import argparse
# from mach_O import get_macho_info
import logging
import logging.handlers
import os
import sys
import time

from .cap import entry_cap
from .date__time import get_date_time
from .mytimer import dynamic_countdown
from .YARA import yara_entry

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def check_os():
    def os_type():
        try:
            # check current System
            if os.name == 'posix':
                logger.info('\033[1;35mRunning on unix system\033[0m')

            elif os.name == 'nt':
                logger.info('\033[1;35mRunning on windows system\033[0m')
                # show additional information
            else:
                logger.info('\033[1;33mRunning on unidentified System')
        except KeyboardInterrupt as e:
            print(f'{e}\nExiting')
            time.sleep(1)
        except Exception as e:
            print(f'{e}')
    return os_type


def add_rule():
    def r_add(rule):
        import importlib.resources as impres
        import subprocess
        rules_folder = impres.files('MDART').joinpath('rules')

        def verify():
            # check whether the rule was added successfully
            if os.path.exists(rules_folder.joinpath(rule)):
                print("Status: \033[1;92mOk\033[0m")
                sys.exit(0)
            p, f = os.path.split(rule)
            if os.path.exists(rules_folder.joinpath(f)):
                print("Status: \033[1;92mOk\033[0m")
                sys.exit(0)
            else:
                print("Status: \033[92mfail\033[0m")
                sys.exit(1)
        try:
            if os.path.isfile(rule) or os.path.isdir(rule):
                full_path = os.path.abspath(rule)
                if os.path.exists(full_path):
                    subprocess.run(['cp', full_path, rules_folder])
            else:
                with open('rule.yara', 'a') as f:
                    f.write(rule)
                abs_fpath = os.path.abspath(rule)
                subprocess.run(['cp', abs_fpath, rules_folder])
        finally:
            verify()
    return r_add


def see_log():
    if os.name == 'posix':
        log = f'/home/{os.getlogin()}/.ThreatHunter/log'

        if os.path.exists(log):
            print(f'\033[1;32mCheck log file at \
\033[1;34m[\033[0m{log}\033[1;34m]\033[1;32m for any redlines \
\033[1;33m{get_date_time()}')

    elif os.name == 'nt':
        log = 'C:\\Users\\ThreatHunter\\log'

        if os.path.exists(log):
            print(f'mCheck log file at   for \
------[{log}]-----any redlines\t{get_date_time()}')


def main():
    parser = argparse.ArgumentParser(description='''MDART is a Malware:
Detection-Analysis-Reverse-Engineering-Toolkit''')

    parser.add_argument('-p', '--path', help='''scan a given directory or file
example \033[1;93mThreatHunter -p /home/user\033[0m''')

    parser.add_argument('-a', '--add', help='''add a new rule to existing yara
rules example \033[1;93mThreatHunter --add rule.yara\033[0m''')

    parser.add_argument('-u', '--use', help='''Provide rule file to match
instead of the default rules example
\033[1;93mThreatHunter -p /home/user/ --use file.yara\033[0m''')
    parser.add_argument(
        '--verbose', '-v', action='store_true', help='''Enable verbose mode,
screen will output hundrends of line , no screen cleaning example;
\033[1;93mThreatHunter --path -v\033[0m''')

    args = parser.parse_args()
    dir_path = args.path
    verbosity = args.verbose

    try:
        os_type = check_os()
        os_type.__call__()
        logger.info('Commencing scan in:')
        dynamic_countdown(2)
    except KeyboardInterrupt:
        print('\nExiting')
        sys.exit(1)

    except Exception as e:
        print(f'{e}')

    if args.add:
        adr = add_rule()
        adr.__call__(args.add)
    if args.path:
        # Try using yara or capstone or redare2
        try:
            if verbosity:
                if args.use:
                    logger.info('\033[1;32mCalling \033[1;35mYARA\033[0m in exclusive mode')
                    yara_entry(dir_path, args.use, True)
                else:
                    # use yara
                    logger.info('\033[1;32mCalling \033[1;35mYARA\033[0m')
                    yara_entry(dir_path, None, True)
                    logger.info(
                        '\033[1;32mCalling \033[1;35mCapstone\033[0m')
                    entry_cap(dir_path, True)
                    logger.info(
                        '\033[1;32mCalling \033[1;35mRedare2\033[0m')
            else:
                if args.use:
                    logger.info('\033[1;32mCalling \033[1;35mYARA\033[0m in exclusive mode')
                    yara_entry(dir_path, args.use, True)
                else:
                    # use yara
                    logger.info('\033[1;32mCalling \033[1;35mYARA\033[0m')
                    yara_entry(dir_path, None)
                    logger.info(
                        '\033[1;32mCalling \033[1;35mCapstone\033[0m')
                    entry_cap(dir_path)
                    logger.info(
                        '\033[1;32mCalling \033[1;35mRedare2\033[0m')
        except KeyboardInterrupt as e:
            print(f'{e}\nExiting')
            time.sleep(1)
        except Exception as e:
            print(f'{e}')
        finally:
            see_log()

    elif args.use:
        print("\033[1;93mCall yara in exclusive mode\033[0m")
        yara_entry(dir_path, args.use, True)

    else:
        try:
            root_dir = os.getcwd()
            if verbosity:
                print(f'current directory = {root_dir}')
                # use yara
                logger.info('\033[1;32mCalling \033[1;35mYARA\033[0m')
                yara_entry(root_dir, True)
                logger.info(
                    '\033[1;32mCalling \033[1;35mCapstone\033[0m')
                entry_cap(root_dir, True)
            else:
                print(f'current directory = {root_dir}')
                # use yara
                logger.info('\033[1;32mCalling \033[1;35mYARA\033[0m')
                yara_entry(root_dir)
                logger.info(
                    '\033[1;32mCalling \033[1;35mCapstone\033[0m')
                entry_cap(root_dir)
        except KeyboardInterrupt as e:
            print(f'{e}\nExiting')
            see_log()
            time.sleep(1)
            sys.exit(1)
        except Exception as e:
            print(f'{e}')
        finally:
            see_log()


if __name__ == '__main__':
    main()
