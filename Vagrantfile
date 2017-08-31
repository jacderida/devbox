# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provision "shell", path: "setup.sh"

  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.vm.box = "ubuntu/xenial64"
    ubuntu.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/ubuntu/.ssh/id_rsa"
    ubuntu.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "ubuntu"
      }
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
  end
  config.vm.define "debian" do |debian|
    debian.vm.box = "debian/jessie64"
    debian.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    debian.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant"
      }
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
  end
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
  end
end
