# -*- mode: ruby -*-
# vi: set ft=ruby :
class String
  def to_bool
    return true   if self == true   || self =~ (/(true|t|yes|y|1)$/i)
    return false  if self == false  || self.empty? || self =~ (/(false|f|no|n|0)$/i)
    raise ArgumentError.new("invalid value for Boolean: \"#{self}\"")
  end
end

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
  config.vbguest.auto_update = false
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http = ENV['VAGRANT_HTTP_PROXY']
    config.proxy.https = ENV['VAGRANT_HTTP_PROXY']
    config.proxy.no_proxy = ENV['VAGRANT_NO_PROXY']
  end
  if ENV['DEVBOX_CORPORATE_MODE']
    config.vm.provision "shell", path: "install_ssl_cert.sh" do |s|
      s.args = "corp.crt"
    end
  end
  config.vm.define "ubuntu" do |ubuntu|
    if ENV['DEVBOX_CORPORATE_MODE']
      ubuntu.vm.provision "shell", path: "./sh/setup_debian.sh", args: ["vagrant", "true", "#{ansible_provisioner}"]
    else
      ubuntu.vm.provision "shell", path: "./sh/setup_debian.sh", args: ["vagrant", "false", "#{ansible_provisioner}"]
    end
    ubuntu.vm.box = "ubuntu/bionic64"
    ubuntu.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    ubuntu.vm.provision "shell", inline: <<SCRIPT
    [[ ! -d "/home/vagrant/dev" ]] && mkdir /home/vagrant/dev
    chown vagrant:vagrant /home/vagrant/dev
SCRIPT
    ubuntu.vm.provision ansible_provisioner do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant",
        corporate_mode: "#{ENV['DEVBOX_CORPORATE_MODE']}".to_bool,
        bare_metal_mode: "#{ENV['DEVBOX_BARE_METAL_MODE']}".to_bool,
        http_proxy: "#{ENV['VAGRANT_HTTP_PROXY']}",
        https_proxy: "#{ENV['VAGRANT_HTTPS_PROXY']}",
        no_proxy: "#{ENV['VAGRANT_NO_PROXY']}",
        ansible_python_interpreter: "/usr/bin/python3"
      }
      ansible.skip_tags = ENV['ANSIBLE_SKIP_TAGS']
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    ubuntu.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      if ENV['DEVBOX_GUI'] == 'true'
        vb.gui = true
        vb.customize ["modifyvm", :id, "--vram", "64"]
        vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
        vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
        vb.customize ["storageattach", :id, "--storagectl", "IDE", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", "emptydrive"]
      end
    end
  end
  config.vm.define "debian" do |debian|
    if ENV['DEVBOX_CORPORATE_MODE']
      debian.vm.provision "shell", path: "./sh/setup_debian.sh", args: ["vagrant", "true", "#{ansible_provisioner}"]
    else
      debian.vm.provision "shell", path: "./sh/setup_debian.sh", args: ["vagrant", "false", "#{ansible_provisioner}"]
    end
    debian.vm.box = "debian/stretch64"
    debian.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    debian.vm.provision "shell", inline: <<SCRIPT
    [[ ! -d "/home/vagrant/dev" ]] && mkdir /home/vagrant/dev
    chown vagrant:vagrant /home/vagrant/dev
SCRIPT
    debian.vm.provision ansible_provisioner do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant",
        corporate_mode: "#{ENV['DEVBOX_CORPORATE_MODE']}".to_bool,
        bare_metal_mode: "#{ENV['DEVBOX_BARE_METAL_MODE']}".to_bool,
        http_proxy: "#{ENV['VAGRANT_HTTP_PROXY']}",
        https_proxy: "#{ENV['VAGRANT_HTTPS_PROXY']}",
        no_proxy: "#{ENV['VAGRANT_NO_PROXY']}"
      }
      ansible.skip_tags = ENV['ANSIBLE_SKIP_TAGS']
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    debian.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      if ENV['DEVBOX_GUI'] == 'true'
        vb.gui = true
        vb.customize ["modifyvm", :id, "--vram", "64"]
        vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
        vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
        vb.customize ["storageattach", :id, "--storagectl", "SATA Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", "emptydrive"]
      end
    end
  end
  config.vm.define "fedora" do |fedora|
    fedora.vm.box = "fedora/28-cloud-base"
    fedora.vm.provision "file", source: "~/.ssh/id_rsa", destination: "/home/vagrant/.ssh/id_rsa"
    fedora.vm.provision "shell", inline: <<SCRIPT
    [[ ! -d "/home/vagrant/dev" ]] && mkdir /home/vagrant/dev
    chown vagrant:vagrant /home/vagrant/dev
    chmod 0600 /home/vagrant/.ssh/id_rsa
SCRIPT
    if ENV['DEVBOX_CORPORATE_MODE']
      fedora.vm.provision "shell", path: "./sh/setup_fedora.sh", args: ["vagrant", "true"]
    else
      fedora.vm.provision "shell", path: "./sh/setup_fedora.sh", args: ["vagrant", "false"]
    end
    fedora.vm.provision ansible_provisioner do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.extra_vars = {
        dev_user: "vagrant",
        corporate_mode: "#{ENV['DEVBOX_CORPORATE_MODE']}".to_bool,
        bare_metal_mode: "#{ENV['DEVBOX_BARE_METAL_MODE']}".to_bool,
        http_proxy: "#{ENV['VAGRANT_HTTP_PROXY']}",
        https_proxy: "#{ENV['VAGRANT_HTTPS_PROXY']}",
        no_proxy: "#{ENV['VAGRANT_NO_PROXY']}"
      }
      ansible.skip_tags = ENV['ANSIBLE_SKIP_TAGS']
      ansible.raw_arguments = ENV['ANSIBLE_ARGS']
    end
    fedora.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      if ENV['DEVBOX_GUI'] == 'true'
        vb.gui = true
        vb.customize ["modifyvm", :id, "--vram", "64"]
        vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
        vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
        vb.customize ["storageattach", :id, "--storagectl", "IDE", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", "emptydrive"]
      end
    end
  end
end
