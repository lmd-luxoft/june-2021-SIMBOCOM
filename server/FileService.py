import os
import re
import logging
import shutil
from datetime import datetime


def _float_to_datetime(value):
    return datetime.utcfromtimestamp(value)


def _get_full_filename(filename, autocreate=False):
    if re.search(r'(^|[\\/])\.\.($|[\\/])', filename):
        raise ValueError('Incorrect value of filename: {}'.format(filename))

    path = os.getcwd()
    full_filename = os.path.join(path, filename)

    folder = os.path.dirname(full_filename)
    if autocreate and not os.path.exists(folder):
        os.makedirs(folder)

    return full_filename


def change_dir(path, autocreate=True):
    if re.search(r'(^|[\\/])\.\.($|[\\/])', path):
        raise ValueError('Incorrect value of path: {}'.format(path))

    if not os.path.exists(path):
        if autocreate:
            os.mkdir(path)
        else:
            raise RuntimeError('Directory {} is not found'.format(path))
    os.chdir(path)


def get_files():
    path = os.getcwd()

    list_file = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            list_file.append(os.path.join(root, filename))

    result = []
    prefix_size = len(path) + 1
    for full_filename in list_file:
        filename = full_filename[prefix_size:]
        result.append({
            'name': filename,
            'create_date': _float_to_datetime(os.path.getctime(full_filename)),
            'edit_date': _float_to_datetime(os.path.getmtime(full_filename)),
            'size': os.path.getsize(full_filename),
        })

    return result


def get_file_data(filename):
    full_filename = _get_full_filename(filename)

    if not os.path.exists(full_filename):
        raise RuntimeError('File {} does not exist'.format(full_filename))

    with open(full_filename, 'rb') as input_file:
        content = input_file.read()

    return {
            'name': filename,
            'content': content,
            'create_date': _float_to_datetime(os.path.getctime(full_filename)),
            'edit_date': _float_to_datetime(os.path.getmtime(full_filename)),
            'size': os.path.getsize(full_filename)
        }


def create_file(filename, content=None):
    full_filename = _get_full_filename(filename, True)

    if os.path.exists(full_filename):
        logging.warning('file {} already exists')

    with open(full_filename, 'wb') as output_file:
        if content:
            output_file.write(bytes(content))

    return {
            'name': filename,
            'content': content,
            'create_date': _float_to_datetime(os.path.getctime(full_filename)),
            'size': os.path.getsize(full_filename)
        }


def delete_file(filename):
    full_filename = _get_full_filename(filename)
    if not os.path.exists(full_filename):
        raise RuntimeError('File {} does not exist'.format(full_filename))

    if os.path.isdir(full_filename):
        shutil.rmtree(full_filename)
    else:
        os.remove(full_filename)
