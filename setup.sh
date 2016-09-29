#!/usr/bin/env bash

apt-get update -y
apt-get install -y curl git libffi-dev libssl-dev python-dev python-pip

pip install --upgrade pyasn1 setuptools
pip install ansible==2.1.1.0
