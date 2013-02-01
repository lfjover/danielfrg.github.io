import os
import shutil
import distutils
from fabric.api import local

def server():
    os.system("jekyll --server --auto")

def clean():
    ignore = ['.git', '.gitignore', '_source']
    files = os.listdir('../')
    files2 = [os.path.join('../', f) for f in files]
    for fname, fpath in zip(files, files2):
        if fname.startswith('.') or fname.startswith('_'):
            pass
        else:
            print(fname)
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
    src_dir = './_site'
    dest_dir = '../'
    _move(src_dir, dest_dir)

def deploy(commit_msg):
    clean()
    move()
    local("git add . && git commit -am '%s'" % commit_msg)
    local("git push")
    # clean()

