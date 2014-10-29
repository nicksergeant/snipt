Vagrant.configure("2") do |config|
  config.vm.box = "puphpet/ubuntu1404-x64"
  config.vm.hostname = "local.snipt.net"
  config.vm.synced_folder ".", "/var/www/snipt/"
  config.vm.network "forwarded_port", guest: 80, host: 8080
end
