#!/usr/bin/env bash

function activate_virtualenv() {
    [[ ! -d "$WORKON_HOME/devbox" ]] && mkvirtualenv devbox
    workon devbox
    pip install paramiko
    pip install testinfra
}

function start_machines() {
    ANSIBLE_ARGS='--skip-tags=slow' vagrant up
}

function run_tests() {
    rm .vagrant/ssh-config
    vagrant ssh-config ubuntu >> .vagrant/ssh-config
    vagrant ssh-config debian >> .vagrant/ssh-config
    testinfra -v --ssh-config=.vagrant/ssh-config --hosts=ubuntu,debian tests.py
}

activate_virtualenv
start_machines
run_tests
