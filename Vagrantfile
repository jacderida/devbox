# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: <<SCRIPT
  apt-get update -y
  apt-get install -y python-dev
  apt-get install -y python-pip
SCRIPT
  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.vm.box = "ubuntu/xenial64"
    ubuntu.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/ubuntu/.ssh/id_rsa"
    ubuntu.vm.provision "shell", inline: "chown ubuntu:ubuntu /home/ubuntu/dev"
    ubuntu.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "ubuntu"
      }
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    if ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']
      ubuntu.vm.synced_folder "#{ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']}", "/home/ubuntu/dev/nerd-fonts", owner: "ubuntu", group: "ubuntu"
    end
  end
  config.vm.define "debian" do |debian|
    debian.vm.box = "debian/stretch64"
    debian.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    debian.vm.provision "shell", inline: "chown vagrant:vagrant /home/vagrant/dev"
    debian.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant"
      }
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    if ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']
      debian.vm.synced_folder "#{ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']}", "/home/vagrant/dev/nerd-fonts", owner: "vagrant", group: "vagrant"
    end
  end
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    if ENV['DEVBOX_GUI'] == 'true'
      vb.gui = true
      vb.customize ["modifyvm", :id, "--vram", "64"]
      vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
    end
  end
end
