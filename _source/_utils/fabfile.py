import os
import shutil
import distutils
from fabric.api import local


def convert(iPythonFile):
    os.system("python nbconvert/jekyll.py %s" % iPythonFile)

