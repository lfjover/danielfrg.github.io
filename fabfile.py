import os
import shutil
import distutils

def server():
    # os.system("cd ./source")
    os.system("jekyll ./source ./source/_site --server --auto")

def clean():
    ignore = ['.git', '.gitignore', 'fabfile.py', 'fabfile.pyc',
                'blog.sublime-project', 'blog.sublime-workspace', 'source']
    for f in os.listdir('./'):
        if f not in ignore:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)

def MoveOver(src_dir, dest_dir):
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
    src_dir = './source/_site'
    dest_dir = './'
    MoveOver(src_dir, dest_dir)
    # shutil.move('./source/_site', './')
    # for f in os.listdir('./source/_site'):
        # shutil.copy2(os.path.join('./source/_site', f), './')

