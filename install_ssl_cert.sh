#!/usr/bin/env bash

cert=$1
if [[ -z "${cert// }" ]]; then
    echo "A value must be supplied for the certificate you want to install."
fi

apt-get update -y
cp /vagrant/$cert /usr/local/share/ca-certificates/$cert
update-ca-certificates
