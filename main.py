#!/usr/bin/env python2
import argparse
import json
import datetime
import os
import sys

from server import FileService


def commandline_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', default=os.path.join(os.getcwd(), 'data'),
                        help="working directory (default: 'data' folder)")

    return parser


def command_change_dir():
    path = raw_input('Enter path: ')
    FileService.change_dir(path)
    return 'Activated directory {}'.format(path)


def command_get_files():
    return FileService.get_files()


def command_get_file_data():
    filename = raw_input('Enter filename: ')
    return FileService.get_file_data(filename)


def command_create_file():
    filename = raw_input('Enter filename: ')
    content = raw_input('Enter content: ')
    return FileService.create_file(filename, content)


def command_delete_file():
    filename = raw_input('Enter filename: ')
    return FileService.delete_file(filename)


def command_exit():
    sys.exit(0)


def _json_serializable(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.strftime("%Y.%m.%d %H:%M:%S")
        return serial

    return obj.__dict__


def main():
    parser = commandline_parser()
    params = parser.parse_args(sys.argv[1:])
    path = params.folder
    FileService.change_dir(path)

    dict_command = {
        'create': command_create_file,
        'change_dir': command_change_dir,
        'list': command_get_files,
        'get': command_get_file_data,
        'delete': command_delete_file,
        'exit': command_exit
    }

    while True:
        try:
            command = raw_input("Enter command: ")

            result = dict_command.get(command, lambda: "Unknown command: {}".format(command))()

            print(json.dumps({
                'status': 'success',
                'result': result,
            }, indent=2, sort_keys=True, default=_json_serializable))

        except Exception as err:
            print(str(err))


if __name__ == '__main__':
    main()
