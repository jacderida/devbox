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
    if ENV['NERDFONTS_SHARED_FOLDER_SRC']
      ubuntu.vm.provision "shell", inline: "chown ubuntu:ubuntu /home/ubuntu/dev"
      ubuntu.vm.synced_folder "#{ENV['NERDFONTS_SHARED_FOLDER_SRC']}", "/home/ubuntu/dev/nerd-fonts", owner: "ubuntu", group: "ubuntu"
    end
    ubuntu.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "ubuntu"
      }
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
  end
  config.vm.define "debian" do |debian|
    debian.vm.box = "debian/stretch64"
    debian.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    debian.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant"
      }
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    if ENV['NERDFONTS_SHARED_FOLDER_SRC']
      debian.vm.provision "shell", inline: "chown vagrant:vagrant /home/vagrant/dev"
      debian.vm.synced_folder "#{ENV['NERDFONTS_SHARED_FOLDER_SRC']}", "/home/vagrant/dev/nerd-fonts"
    end
  end
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    if ENV['DEVBOX_GUI'] == 'true'
      vb.gui = true
      vb.customize ["modifyvm", :id, "--vram", "64"]
      vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
    end
  end
end
