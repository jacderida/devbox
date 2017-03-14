# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"
  config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
  config.vm.provision "file", source: "~/.vimrc", destination: "/home/vagrant/.vimrc"
  config.vm.provision "shell", path: "setup.sh"
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.extra_vars = {
      dev_user: "vagrant"
    }
  end

   config.vm.provider "virtualbox" do |vb|
     vb.memory = "2048"
   end
end
