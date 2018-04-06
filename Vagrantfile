# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/xenial64"

  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8080, host: 8080

  config.vm.provision "shell", inline: <<-SHELL
    # Update and upgrade the server packages.
    sudo apt-get update
    sudo apt-get -y upgrade
    # Set Ubuntu Language
    sudo locale-gen en_GB.UTF-8
    # Install Python, SQLite and pip
    sudo apt-get install -y python3-dev sqlite python3-pip
    # Upgrade pip to the latest version.
    sudo pip3 install --upgrade pip
    # Install and configure python virtualenvwrapper.
    sudo pip3 install virtualenvwrapper
    if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
        echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
        echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
        echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
        echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
    fi
    sudo pip3 install django
    wget "https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh"

    # Prefix should default to /home/vagrant/anaconda3
    # sudo cp /vagrant/Anaconda3-5.1.0-Linux-x86_64.sh /home/vagrant/
    sudo bash Anaconda3-5.1.0-Linux-x86_64.sh -b -p /home/vagrant/anaconda
    # rm Anaconda3-5.1.0-Linux-x86_64.sh
    sudo chown -R vagrant:vagrant /home/vagrant/anaconda
    echo 'export PATH="/home/vagrant/anaconda/bin:$PATH"' >> /home/vagrant/.bashrc

    sudo /home/vagrant/anaconda/bin/conda update conda

  SHELL

end