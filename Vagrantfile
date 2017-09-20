# -*- mode: ruby -*-
# vi: set ft=ruby :

module OS
  def OS.windows?
    (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
  end
  def OS.mac?
    (/darwin/ =~ RUBY_PLATFORM) != nil
  end
  def OS.unix?
    !OS.windows?
  end
  def OS.linux?
    OS.unix? and not OS.mac?
  end
end

ansible_provisioner = OS.windows? ? "ansible_local" : "ansible"

Vagrant.configure("2") do |config|
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http = ENV['VAGRANT_HTTP_PROXY']
    config.proxy.https = ENV['VAGRANT_HTTP_PROXY']
    config.proxy.no_proxy = ENV['VAGRANT_NO_PROXY']
  end
  config.vm.provision "shell", path: "install_ssl_cert.sh" do |s|
    s.args = "corp.crt"
  end
  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.vm.box = "ubuntu/xenial64"
    ubuntu.vm.provision "shell", path: "setup.sh" do |s|
      s.args = "ubuntu"
    end
    ubuntu.vm.provision ansible_provisioner do |ansible|
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
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
    end
  end
end
