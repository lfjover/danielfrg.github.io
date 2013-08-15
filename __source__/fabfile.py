import os
import shutil
from fabric.api import local


def build():
    local('pelican content/ -o output/ -s pelicanconf.py')


def serve():
    local('cd output && python -m pelican.server')


def clean():
    local('make clean')
    # --
    file_names = os.listdir('../')
    file_paths = [os.path.join('../', f) for f in file_names]
    for fname, fpath in zip(file_names, file_paths):
        if fname.startswith('.') or fname.startswith('_'):
            pass
        else:
            if os.path.isdir(fpath):
                shutil.rmtree(fpath)
            else:
                os.remove(fpath)


def _move(src_dir, dest_dir):
    fileList = os.listdir(src_dir)
    for i in fileList:
        src = os.path.join(src_dir, i)
        dest = os.path.join(dest_dir, i)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                _move(src, dest)
                continue
            else:
                os.remove(dest)
        shutil.move(src, dest_dir)


def move():
    # local('mv output/* ../')  # maybe?
    src_dir = './output'
    dest_dir = '../'
    _move(src_dir, dest_dir)


def update():
    clean()
    local('make html')
    move()
    # local("git push")
    # clean()
