# this is the begining of a deploy script... it is far from done

import pickle
import shutil
import os
import subprocess

try:
    shutil.rmtree('wp')
except FileNotFoundError:
    pass

os.mkdir('wp')

shutil.copy('main.py', 'wp/main.py')
shutil.copytree('source', 'wp/source')
shutil.copytree('assets', 'wp/assets')






