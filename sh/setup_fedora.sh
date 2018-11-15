#!/usr/bin/env bash

dnf update -y
dnf install -y python python-dnf
dnf install -y python3-libselinux python2-libselinux
dnf install -y libffi-devel openssl-devel python-devel redhat-rpm-config

pip install --upgrade pip
pip install ansible
