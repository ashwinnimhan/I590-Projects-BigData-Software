#!/bin/bash

echo "clone git repository ::"
	git clone https://github.iu.edu/animhan/sw-project-template.git --recursive
	git clone https://github.com/futuresystems/big-data-stack.git --recursive

echo "load parameters ::"
	module load openstack
	source ~/CH-817724-openrc.sh
	source $HOME/bdossp_sp16/bin/activate

echo "setup ssh options ::"
	eval $(ssh-agent)
	ssh-add

echo "configure big-data-stack ::"
	cp ./sw-project-template/src/{.cluster.py,ansible.cfg,site.yml} ./big-data-stack/
 
echo "install big-data-stack dependencies ::"
	pip install -r ./big-data-stack/requirements.txt
	
echo "create instances ::"
	vcl boot -p openstack -P $USER-
	sleep 20

echo "check status of instances ::"
	ansible all -m ping

echo "setup hadoop and spark ::"
	ansible-playbook play-hadoop.yml
	ansible-playbook addons/spark.yml

echo "deploy artifacts(dataset) ::"
	cd ./big-data-stack
	ansible-playbook site.yml