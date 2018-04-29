#!/usr/bin/env bash

cert=$1
if [[ -z "${cert// }" ]]; then
    echo "A value must be supplied for the certificate you want to install."
fi

function install_debian() {
    apt-get update -y
    cp /vagrant/$cert /usr/local/share/ca-certificates/$cert
    update-ca-certificates
}

function install_fedora() {
    yum update -y
    yum install -y ca-certificates
    cp /vagrant/$cert /etc/pki/ca-trust/source/anchors/$cert
    update-ca-trust
}

# Obviously this needs to be updated to select the operating system.
install_debian
