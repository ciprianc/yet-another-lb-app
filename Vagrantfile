VAGRANTFILE_API_VERSION = "2"
box_name = 'ubuntu/xenial64'
domain   = 'local'

nodes = [
  { :hostname => 'app-1',  :ip => '192.168.50.10'},
  { :hostname => 'app-2',  :ip => '192.168.50.11'},
  { :hostname => 'lb',     :ip => '192.168.50.253'},
]

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  nodes.each do |node|
    config.vm.define node[:hostname] do |box|
        box.vm.box = box_name
        box.vm.hostname = node[:hostname] + '.' + domain
        box.vm.network "private_network", ip: node[:ip], virtualbox__intnet: true
        # try to get each node's memory setting, default to 256
        box.vm.provider :virtualbox do |vb|
            vb.memory = node[:ram] ? node[:ram] : 256
            vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
        if node[:hostname] == 'lb'
            box.vm.network "forwarded_port", guest: 80, host: 65080, auto_correct: true
        end
    end
  end

  # try apt-get update, try and install puppet even if update failed
  config.vm.provision "shell",
      inline: "apt update ; DEBIAN_FRONTEND=noninteractive apt -yq install python-simplejson"

  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "provisioning/playbook.yml"
    ansible.groups = {
     "apps" => ["app-[1:2]"],
     "lbs" => ["lb"],
     "all_groups:children" => ["apps", "lb"],
     "lbs:vars" => {"upstreams" => ["192.168.50.10", "192.168.50.11"]}
    }
  end

end
