#!/usr/bin/env bash

dev_user=$1
if [[ -z "${dev_user// }" ]]; then
    echo "A value must be supplied for the dev_user"
    exit 1
fi
corporate_mode=$2
if [[ -z "${corporate_mode// }" ]]; then
    echo "A value must be supplied for corporate mode (true or false)"
fi
ansible_provisioner=$3
if [[ -z "${ansible_provisioner// }" ]]; then
    echo "A value must be supplied for ansible provisioner"
fi

function install_ansible_prerequisites() {
    if [[ "$ansible_provisioner" == "ansible_local" ]]; then
        apt-get install -y curl libffi-dev libssl-dev python-dev python-pip
    fi
}

function install_ansible() {
    if [[ "$ansible_provisioner" == "ansible_local" ]]; then
        if [[ "$corporate_mode" == "true" ]]; then
            pip install --upgrade pyasn1 setuptools --cert /usr/local/share/ca-certificates/corp.crt
            pip install ansible==2.7.1 --cert /usr/local/share/ca-certificates/corp.crt
        else
            pip install --upgrade pyasn1 setuptools
            pip install ansible==2.7.1
        fi
    fi
}

function setup_git() {
    # Git comes installed with Ubuntu (at least the Vagrant box, anyway), and for the proxy
    # environment, it needs to be removed to be replaced with a different version that uses
    # the openssl library rather than gnutls.
    if [[ "$corporate_mode" == "true" ]]; then
        if [[ ! -f "/home/$dev_user/.git_openssl_mod_installed" ]]; then
            apt-get remove git -y
        fi
    fi
}

apt-get update -y
setup_git
install_ansible_prerequisites
install_ansible
