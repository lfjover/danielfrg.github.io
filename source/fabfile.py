import os
import shutil
import distutils
from fabric.api import local

def server():
    os.system("jekyll --server --auto")

def clean():
    ignore = ['.git', '.gitignore', 'source']
    for f in os.listdir('../'):
        if f not in ignore:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)

def _move(src_dir, dest_dir):
    fileList = os.listdir(src_dir)
    for i in fileList:
        src = os.path.join(src_dir, i)
        dest = os.path.join(dest_dir, i)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                MoveOver(src, dest)
                continue
            else:
                os.remove(dest)
        shutil.move(src, dest_dir)

def move():
    src_dir = './_site'
    dest_dir = '../'
    _move(src_dir, dest_dir)

def deploy(commit_msg):
    move()
    local("git add . && git commit -am '%s'" % commit_msg)
    local("git push")
    # clean()

