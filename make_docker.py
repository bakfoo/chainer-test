#!/usr/bin/env python

import argparse

codes = {}

# base

codes['centos7_py2'] = '''FROM centos:7

RUN yum -y update
RUN yum -y install epel-release
RUN yum -y install ccache gcc gcc-c++ git kmod hdf5-devel perl

ENV PATH /usr/lib64/ccache:$PATH

RUN yum -y install python-devel python-pip
'''

codes['centos7_py3'] = '''FROM centos:7

RUN yum -y update
RUN yum -y install epel-release
RUN yum -y install ccache gcc gcc-c++ git kmod hdf5-devel perl

ENV PATH /usr/lib64/ccache:$PATH

RUN yum -y install bzip2-devel make openssl-devel readline-devel
RUN git clone git://github.com/yyuu/pyenv.git /opt/pyenv
ENV PYENV_ROOT=/opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.4.3
RUN pyenv global 3.4.3
RUN pyenv rehash
'''

codes['ubuntu14_py2'] = '''FROM ubuntu:14.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y ccache curl g++ gfortran git libhdf5-dev

ENV PATH /usr/lib/ccache:$PATH

RUN apt-get install -y python-pip python-dev
'''

codes['ubuntu14_py3'] = '''FROM ubuntu:14.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y ccache curl g++ gfortran git libhdf5-dev

ENV PATH /usr/lib/ccache:$PATH

RUN apt-get install -y python3-pip python3-dev
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
'''

codes['ubuntu14_py35'] = '''FROM ubuntu:14.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y ccache curl g++ gfortran git libhdf5-dev

ENV PATH /usr/lib/ccache:$PATH

RUN apt-get -y install libbz2-dev libreadline-dev libssl-dev make
RUN git clone git://github.com/yyuu/pyenv.git /opt/pyenv
ENV PYENV_ROOT=/opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.5.0
RUN pyenv global 3.5.0
RUN pyenv rehash
'''

# numpy

codes['numpy19'] = '''
RUN pip install numpy==1.9.3
'''

codes['numpy110'] = '''
RUN pip install numpy==1.10.2
'''

# cuda

cuda65_run = 'cuda_6.5.19_linux_64.run'
cuda65_url = 'http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers'
cuda65_installer = 'cuda-linux64-rel-6.5.19-18849900.run'

cuda70_run = 'cuda_7.0.28_linux.run'
cuda70_url = 'http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers'
cuda70_installer = 'cuda-linux64-rel-7.0.28-19326674.run'

cuda75_run = 'cuda_7.5.18_linux.run'
cuda75_url = 'http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers'
cuda75_driver = 'NVIDIA-Linux-x86_64-352.39.run'
cuda75_installer = 'cuda-linux64-rel-7.5.18-19867135.run'

cuda_base = '''
WORKDIR /opt/nvidia
RUN mkdir installers

RUN curl -s -o {cuda_run} {cuda_url}/{cuda_run}
RUN curl -s -o {cuda75_run} {cuda75_url}/{cuda75_run}

RUN chmod +x {cuda75_run} && sync && \\
    ./{cuda75_run} -extract=`pwd`/installers
RUN ./installers/{driver} -s -N --no-kernel-module

RUN chmod +x {cuda_run} && sync && \\
    ./{cuda_run} -extract=`pwd`/installers
RUN ./installers/{installer} -noprompt

RUN cd / && \\
    rm -rf /opt/nvidia

ENV CUDA_ROOT /usr/local/cuda
ENV PATH $PATH:$CUDA_ROOT/bin
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$CUDA_ROOT/lib64
'''

cuda75_base = '''
WORKDIR /opt/nvidia
RUN mkdir installers

RUN curl -s -o {cuda_run} {cuda_url}/{cuda_run}

RUN chmod +x {cuda_run} && sync && \\
    ./{cuda_run} -extract=`pwd`/installers

RUN ./installers/{driver} -s -N --no-kernel-module && \\
    ./installers/{installer} -noprompt && \\
    cd / && \\
    rm -rf /opt/nvidia

ENV CUDA_ROOT /usr/local/cuda
ENV PATH $PATH:$CUDA_ROOT/bin
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$CUDA_ROOT/lib64
'''

codes['cuda65'] = cuda_base.format(
    cuda_run=cuda65_run,
    cuda_url=cuda65_url,
    cuda75_run=cuda75_run,
    cuda75_url=cuda75_url,
    driver=cuda75_driver,
    installer=cuda65_installer,
)

codes['cuda70'] = cuda_base.format(
    cuda_run=cuda70_run,
    cuda_url=cuda70_url,
    cuda75_run=cuda75_run,
    cuda75_url=cuda75_url,
    driver=cuda75_driver,
    installer=cuda70_installer,
)

codes['cuda75'] = cuda75_base.format(
    cuda_run=cuda75_run,
    cuda_url=cuda75_url,
    driver=cuda75_driver,
    installer=cuda75_installer,
)

# cudnn

cudnn2_base = '''
WORKDIR /opt/cudnn
RUN curl -s -o {cudnn}.tgz http://developer.download.nvidia.com/compute/redist/cudnn/{cudnn_ver}/{cudnn}.tgz
RUN tar -xzf {cudnn}.tgz
RUN rm {cudnn}.tgz
RUN cp {cudnn}/cudnn.h /usr/local/cuda/include/.
RUN mv {cudnn}/libcudnn.so /usr/local/cuda/lib64/.
RUN mv {cudnn}/libcudnn.so.6.5 /usr/local/cuda/lib64/.
RUN mv {cudnn}/libcudnn.so.6.5.48 /usr/local/cuda/lib64/.
RUN mv {cudnn}/libcudnn_static.a /usr/local/cuda/lib64/.
'''

codes['cudnn2'] = cudnn2_base.format(
    cudnn='cudnn-6.5-linux-x64-v2',
    cudnn_ver='v2',
)

cudnn_base = '''
WORKDIR /opt/cudnn
RUN curl -s -o {cudnn}.tgz http://developer.download.nvidia.com/compute/redist/cudnn/{cudnn_ver}/{cudnn}.tgz
RUN tar -xzf {cudnn}.tgz -C /usr/local
RUN rm {cudnn}.tgz
'''

codes['cudnn3'] = cudnn_base.format(
    cudnn='cudnn-7.0-linux-x64-v3.0-prod',
    cudnn_ver='v3',
)

codes['cudnn4-rc'] = cudnn_base.format(
    cudnn='cudnn-7.0-linux-x64-v4.0-rc',
    cudnn_ver='v4',
)

codes['none'] = ''


def set_env(env, value):
    return 'ENV {}={}\n'.format(env, value)


p = argparse.ArgumentParser()
p.add_argument('--base', choices=['ubuntu14_py2', 'ubuntu14_py3', 'ubuntu14_py35', 'centos7_py2', 'centos7_py3'], required=True)
p.add_argument('--numpy', choices=['numpy19', 'numpy110'], required=True)
p.add_argument('--cuda', choices=['none', 'cuda65', 'cuda70', 'cuda75'], required=True)
p.add_argument('--cudnn', choices=['none', 'cudnn2', 'cudnn3', 'cudnn4-rc'], required=True)
p.add_argument('--requires', action='append')
p.add_argument('--http-proxy')
p.add_argument('--https-proxy')
p.add_argument('-f', '--dockerfile', default='Dockerfile')
args = p.parse_args()

with open(args.dockerfile, 'w') as f:
    f.write(codes[args.base])
    if args.http_proxy:
        f.write(set_env('http_proxy', args.http_proxy))
    if args.https_proxy:
        f.write(set_env('https_proxy', args.https_proxy))
    f.write(codes[args.numpy])
    f.write(codes[args.cuda])
    f.write(codes[args.cudnn])

    if args.requires:
        f.write('\n')
        for r in args.requires:
            f.write('RUN pip install %s\n' % r)
