import os
import textwrap
from setuptools import setup, find_packages
import subprocess

# Semantic versioning
MAJOR = 0
MINOR = 4
PATCH = 0
IS_RELEASED = False

VERSION = '{0}.{1}.{2}'.format(MAJOR, MINOR, PATCH)

def git_short_hash():
    """ Returns the short hash of the latest git commit as a string. """

    git_str = subprocess.check_output(['git', 'log', '-1',
        '--format=%h']).decode('UTF-8').strip()
    return git_str

FULL_VERSION = VERSION
if not IS_RELEASED:
    FULL_VERSION += '+' + git_short_hash()

def write_version_module(version_path='maxwellbloch/version.py'):
    """ Write a version module with the current version."""

    # Remove if already exists
    if os.path.exists(version_path):
        os.remove(version_path)

    version_str = textwrap.dedent("""\
        # This file is generated by setup.py
        VERSION = '{!s}'
        FULL_VERSION = '{!s}'
        IS_RELEASED = {!s}
        """.format(VERSION, FULL_VERSION, IS_RELEASED))

    f = open(version_path, 'w')
    try:
        f.write(version_str)
    finally:
        f.close()

write_version_module()

setup(name='MaxwellBloch',
      version=FULL_VERSION,
      description='A Python package for solving the Maxwell-Bloch equations.',
      url='http://github.com/tommyogden/maxwellbloch',
      author='Thomas P Ogden',
      author_email='t@ogden.eu',
      license='MIT',
      packages=find_packages(),
      package_data={'maxwellbloch.tests': ['json/*.json']},
      install_requires=['qutip'],
      scripts=['bin/make-mp4-fixed-frame.py',
               'bin/make-gif-ffmpeg.sh'],
      zip_safe=False)
