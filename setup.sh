#!/usr/bin/env bash

dev_user=$1
if [[ -z "${dev_user// }" ]]; then
    echo "A value must be supplied for the dev_user."
    exit 1
fi

function install_ansible_prerequisites() {
    apt-get update -y
    apt-get install -y curl libffi-dev libssl-dev python-dev python-pip
}

function install_ansible() {
    pip install --upgrade pip --cert /usr/local/share/ca-certificates/slc.crt
    pip install --upgrade pyasn1 setuptools --cert /usr/local/share/ca-certificates/slc.crt
    pip install ansible==2.1.1.0 --cert /usr/local/share/ca-certificates/slc.crt
}

function setup_git() {
    # Git comes installed with Ubuntu (at least the Vagrant box, anyway), and for the proxy
    # environment, it needs to be removed to be replaced with a different version that uses
    # the openssl library rather than gnutls.
    # This needs an extra conditional to detect proxy mode.
    if [[ ! -f "/home/$dev_user/.git_openssl_mod_installed" ]]; then
        apt-get remove git -y
    fi
}

setup_git
install_ansible_prerequisites
install_ansible
