#!/usr/bin/env bash

apt-get update -y
apt-get remove git -y
apt-get install -y curl libffi-dev libssl-dev python-dev python-pip

pip install --upgrade pip --cert /usr/local/share/ca-certificates/slc.crt
pip install --upgrade pyasn1 setuptools --cert /usr/local/share/ca-certificates/slc.crt
pip install ansible==2.1.1.0 --cert /usr/local/share/ca-certificates/slc.crt
