---
title: "Siesta Install"
description: ""
date: "2023-03-20T23:03:47+08:00"
thumbnail: ""
categories:
  - ""
tags:
  - ""
sidebar: true
---


Main reference to [Centos6.6系统里安装SIESTA 4 | 知乎](https://zhuanlan.zhihu.com/p/22834848) 。  
Related software and libraries are installed under `~/software` if not otherwise specified.

## system and environment

```
Linux version 5.15.90.1-microsoft-standard-WSL2 (oe-user@oe-host) (x86_64-msft-linux-gcc (GCC) 9.3.0, GNU ld (GNU Binutils) 2.34.0.20200220) #1 SMP Fri Jan 27 02:56:13 UTC 2023

Ubuntu 20.04.4 LTS
```

GCC already installed

## openmpi

```bash
# download and unzip
wget https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-3.1.4.tar.gz
tar -xzvf openmpi-3.1.4.tar.gz
cd openmpi-3.1.4
# config and install
mkdir ~/software/openmpi/3.1.4
./configure --prefix=~/software/openmpi/3.1.4
make
make install
# profile
vi ~/.zshrc.local ## i use zsh; for bash it's ~/.bashrc or ~/.bashrc.local
## add following commands
OPENMPI=~/software/openmpi/3.1.4
export LD_LIBRARY_PATH=$OPENMPI/lib:$LD_LIBRARY_PATH
export PATH=$OPENMPI/bin:$PATH
export INCLUDE=$OPENMPI/include:$INCLUDE
export CPATH=$OPENMPI/include:$CPATH
export MANPATH=$OPENMPI/share/man:$MANPATH
## exit vim
source ~/.zshrc # or source ~/.bashrc
# test
ompi_info | grep Ident # version
cd ~/software/openmpi/3.1.4/examples
make
./hello_c
```

## mpiblacs

```bash
# download and unzip
wget http://www.netlib.org/blacs/mpiblacs.tgz
tar -zxvf mpiblacs.tgz
cd BLACS
# config and make
cp BMAKES/Bmake.MPI-LINUX ./Bmake.inc
vi Bmake.inc
## modify some lines as
INTFACE  = -DAdd_
MPIdir = ~/software/openmpi/3.1.4
MPILIBdir = $(MPIdir)/lib # !! delet the last / !!
MPILIB = $(MPILIBdir)/libmpi.so # some people think it should be libmpi.a but i only find libmpi.so under the lib and it works
F77 = mpif90
## exit vim
make
# test
make mpi tester
make mpi what=clean
# ------
# NOTE:
# 1. you will find blacs_MPI-LINUX-0.a under BLACS/LIB if success
# 2. if it prints Error and exits during making, check the file path. You can temporarily move the folder BLACS to a suitable place and move back after making.
# ------
```

## lapack

```bash
# download and unzip
wget http://www.netlib.org/lapack/lapack-3.6.1.tgz
tar -zxvf lapack-3.6.1.tgz
cd lapack-3.6.1
# config and make
cp make.inc.example make.inc
vi make.inc
## modify two lines (annotating and un-annotating) as
# TIMER = INT_ETIME # !! annotating !!
TIMER = NONE # !! un-annotating !!
## exit vim
vi Makefile
## modify two lines as
# lib: lapacklib tmglib # !! annotating !!
lib: blaslib lapacklib tmglib # !! un-annotating and delete variants !!
## exit vim
make
# ------
# NOTE:
# 1. you will get liblapack.a, librefblas.a, libtmglib.a if success
# 2. if it prints Error about znep.out ans exits during making, try run `ulimit -s unlimited` in command line.
# ------
## the following commands may need sudo
cp ./liblapack.a /usr/lib
cp ./liblapack.a /usr/local/lib
cp ./librefblas.a /usr/lib/libblas.a # !! rename !!
cp ./librefblas.a /usr/local/lib/libblas.a # !! rename !!
cp ./libtmglib.a /usr/lib
cp ./libtmglib.a /usr/local/lib
```

## scalapack

```bash
# download and unzip
wget http://www.netlib.org/scalapack/scalapack.tgz
tar -zxvf scalapack.tgz
cd scalapack-2.2.0
# config and make
cp SLmake.inc.example SLmake.inc
make
make exe
# ------
# you will get libscalapack.a if success
# ------
```

## siesta

```bash
# download and unzip
wget https://launchpad.net/siesta/4.0/4.0.2/+download/siesta-4.0.2.tar.gz
tar -zxvf siesta-4.0.2.tar.gz
cd siesta-4.0.2
# config and make
cd ./Obj
../Src/obj_setup.sh
../Src/configure \
	--enable-mpi FC=~/software/openmpi/3.1.4/bin/mpif90 \
	--with-blacs=~/software/BLACS/LIB/blacs_MPI-LINUX-0.a \
	--with-scalapack=~/software/scalapack-2.2.0/libscalapack.a
make
# ------
# you will get a file named siesta if success
# you can copy it every where you want in the system or build softlink
# ------
# test
cd ./Tests
vi test.mk
## modify SIESTA, for example
SIESTA= mpirun -np 16 --oversubscribe ~/software/Obj/siesta
## exit vim
make
```

