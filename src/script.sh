#!/bin/bash

echo "clone git repository ::"
	git clone https://github.iu.edu/animhan/sw-project-template.git --recursive
	git clone https://github.com/futuresystems/big-data-stack.git --recursive

echo "load parameters ::"
	cd ./sw-project-template/src
	module load openstack
	source ./CH-817724-openrc.sh
	source $HOME/bdossp_sp16/bin/activate

echo "setup ssh options ::"
	eval $(ssh-agent)
	ssh-add

echo "configure big-data-stack ::"
	cp {.cluster.py,ansible.cfg,site.yml} ../../big-data-stack/
 
echo "install big-data-stack dependencies ::"
	cd ../../big-data-stack
	pip install -r requirements.txt
	
echo "create instances ::"
	vcl boot -p openstack -P $USER-
	sleep 20

echo "check status of instances ::"
	ansible all -m ping

echo "setup hadoop and spark ::"
	ansible-playbook play-hadoop.yml
	ansible-playbook addons/spark.yml

echo "deploy artifacts(dataset) ::"
	cd ../sw-project-template/src
	ansible-playbook site.yml

echo "ssh into master node ::"
echo "switch user: sudo su - hadoop"
echo "Execute: spark-submit --master yarn --deploy-mode client /tmp/scripts/clickstream.py"
echo "Execute: spark-submit --master yarn --deploy-mode client /tmp/scripts/pageviews.py"
	vcl ssh master0 -- -l cc sudo su