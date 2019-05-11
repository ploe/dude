# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.hostname = "mantis"

  config.vm.network "private_network", ip: "10.3.13.100"
  config.vm.network "forwarded_port", guest: 3306, host: 3306

  config.vm.provision "shell", inline: "sudo apt update && sudo apt upgrade -y && sudo apt -y install docker.io docker-compose"
  config.vm.provision "shell", inline: "sudo usermod -aG docker vagrant"

  config.vm.provider "virtualbox" do |vb|
     vb.memory = "4096"
  end
end
