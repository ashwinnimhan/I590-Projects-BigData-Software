#!/bin/bash

# clone git repository ::
	git clone https://github.iu.edu/animhan/sw-project-template.git --recursive
	git clone https://github.com/futuresystems/big-data-stack.git --recursive

# load parameters ::
	cd ./sw-project-template/src
	
	module load openstack
	cp ./CH-817724-openrc.sh ~/
	source ~/CH-817724-openrc.sh
	source $HOME/bdossp_sp16/bin/activate

# setup ssh options ::
	eval $(ssh-agent)
	ssh-add

# configure big-data-stack ::
	cp {.cluster.py,ansible.cfg,site.yml} ../../big-data-stack/
 
# install big-data-stack dependencies ::
	cd ../../big-data-stack
	pip install -r requirements.txt
	
# create instances ::
	vcl boot -p openstack -P $USER-
	sleep 20

# check status of instances ::
	ansible all -m ping

# setup hadoop and spark ::
	ansible-playbook play-hadoop.yml
	ansible-playbook addons/spark.yml

# deploy artifacts(dataset) ::
	ansible-playbook site.yml

# ssh into master node	
	echo "Execute: spark-submit --master yarn --deploy-mode client /tmp/scripts/clickstream.py"
	echo "Execute: spark-submit --master yarn --deploy-mode client /tmp/scripts/pageviews.py"
	vcl ssh master0 -- -l cc sudo su 