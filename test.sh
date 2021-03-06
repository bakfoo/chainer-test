#!/bin/sh -ex

pip install -U pip

cd chainer
python setup.py -q develop install

pip install -q nose mock coverage coveralls

nosetests --processes=4 --process-timeout=10000 --with-coverage --cover-branches --cover-package=chainer,cupy

coverage xml -i

if [ $COVERALLS_REPO_TOKEN ]; then
  coveralls
fi
