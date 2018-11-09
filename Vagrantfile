# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.hostname = "mantis"

  config.vm.network "private_network", ip: "10.3.13.100"

  config.vm.provider "virtualbox" do |vb|
     vb.memory = "4096"
  end
end
