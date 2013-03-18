import os
import shutil
import distutils
from fabric.api import local


def clean():
    local('make clean')
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
    src_dir = './output'
    dest_dir = '../'
    _move(src_dir, dest_dir)

def deploy():
    clean()
    local('make html')
    move()
    # local("git push")
    # clean()

