# coding=utf-8
import os
import shutil

import pytest

from server import FileService

TEST_DIR = 'test_dir'


@pytest.fixture('module', autouse=True)
def change_dir_tes():
    old_dir = os.getcwd()
    yield
    os.chdir(old_dir)


def _remove_dir(path):
    if not os.path.exists(path):
        return

    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


@pytest.fixture('function', autouse=True)
def change_dir_tes():
    _remove_dir(TEST_DIR)
    yield
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    _remove_dir(TEST_DIR)


class Test_change_dir:

    def test_incorrect_type1(self):
        with pytest.raises(TypeError):
            FileService.change_dir(None)

    def test_incorrect_type2(self):
        with pytest.raises(TypeError):
            FileService.change_dir(20)

    def test_dot_dir(self):
        old_dir = os.getcwd()
        FileService.change_dir('.')

        assert old_dir == os.getcwd()

    def test_incorrect_value2(self):
        with pytest.raises(ValueError):
            FileService.change_dir('..')

    def test_incorrect_value3(self):
        with pytest.raises(ValueError):
            FileService.change_dir('../something')

    def test_existing_dir_no_create(self):
        os.mkdir(TEST_DIR)
        FileService.change_dir('test_dir', False)
        assert os.path.basename(os.getcwd()) == TEST_DIR

    def test_existing_dir_create(self):
        """Перейти в каталог, который уже существует и autocreate=True

        Ожидаемый результат: текущая папка имеет имя ExistingDirectory
        """
        os.mkdir(TEST_DIR)
        FileService.change_dir(TEST_DIR, True)
        assert os.path.basename(os.getcwd()) == TEST_DIR

    def test_non_existing_dir_no_create(self):
        """Перейти в каталог, который не существует и autocreate=False

        Ожидаемый результат: текущая папка имеет имя отличное от NotExistingDirectory
        """
        with pytest.raises(RuntimeError):
            FileService.change_dir(TEST_DIR, False)
        print(os.path.basename(os.getcwd()))
        assert os.path.basename(os.getcwd()) != TEST_DIR

    def test_non_existing_dir_create(self):
        """Перейти в каталог, который не существует и autocreate=True

        Ожидаемый результат: текущая папка имеет имя отличное от NotExistingDirectory
        """
        FileService.change_dir(TEST_DIR, True)
        assert os.path.basename(os.getcwd()) == TEST_DIR
