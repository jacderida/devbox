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
    ubuntu.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/ubuntu/.ssh/id_rsa"
    ubuntu.vm.provision "shell", inline: <<SCRIPT
    [[ ! -d "/home/ubuntu/dev" ]] && mkdir /home/ubuntu/dev
    chown ubuntu:ubuntu /home/ubuntu/dev
SCRIPT
    ubuntu.vm.provision ansible_provisioner do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "ubuntu"
      }
      ansible.skip_tags = ENV['ANSIBLE_SKIP_TAGS']
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    if ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']
      ubuntu.vm.synced_folder "#{ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']}", "/home/ubuntu/dev/nerd-fonts", owner: "ubuntu", group: "ubuntu"
    end
  end
  config.vm.define "debian" do |debian|
    debian.vm.box = "debian/stretch64"
    debian.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    debian.vm.provision "shell", inline: <<SCRIPT
    [[ ! -d "/home/vagrant/dev" ]] && mkdir /home/vagrant/dev
    chown vagrant:vagrant /home/vagrant/dev
SCRIPT
    debian.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant"
      }
      ansible.skip_tags = ENV['ANSIBLE_SKIP_TAGS']
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    if ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']
      debian.vm.synced_folder "#{ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']}", "/home/vagrant/dev/nerd-fonts", owner: "vagrant", group: "vagrant"
    end
  end
  config.vm.define "fedora" do |fedora|
    fedora.vm.box = "fedora/26-cloud-base"
    fedora.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    fedora.vm.provision "shell", inline: <<SCRIPT
    [[ ! -d "/home/vagrant/dev" ]] && mkdir /home/vagrant/dev
    chown vagrant:vagrant /home/vagrant/dev
    chmod 0600 /home/vagrant/.ssh/id_rsa
SCRIPT
    fedora.vm.provision "shell", path: "sh/setup_fedora.sh"
    fedora.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant"
      }
      ansible.skip_tags = ENV['ANSIBLE_SKIP_TAGS']
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    if ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']
      fedora.vm.synced_folder "#{ENV['DEVBOX_NERDFONTS_SHARED_FOLDER']}", "/home/vagrant/dev/nerd-fonts", owner: "vagrant", group: "vagrant"
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
