======================================
Exploratory Data Analysis of Wikipedia
======================================
******************************
Instructions for deploying
******************************
- Download script.sh from git src folder:
  https://github.iu.edu/animhan/sw-project-template/blob/master/src/script.sh
- Make sure CH-817724-openrc.sh is present under ~/. If it is not present, download it from your Chameleon Cloud Account under API access section.
- Execute : bash script.sh
- Check which node is master node by executing the command: nova list | grep "$USER". The master node will be named as "$USER-master0"
- SSH using the floating IP assigned to the master node.
- Switch to hadoop user using: sudo su - hadoop
- Execute scripts
    - spark-submit --master yarn --deploy-mode client /tmp/scripts/pageviews.py
    - spark-submit --master yarn --deploy-mode client /tmp/scripts/clickstream.py
- The results are accessible in HDFS and can be accessed by the following commands:
    - hadoop dfs -ls /top50WikiArticles
    - hadoop dfs -ls /top50Referers
    - hadoop dfs -ls /top50TrendingOnTwitter
    - hadoop dfs -ls /top50RequestedMissingPages
    - hadoop dfs -ls /top50InflowVsOutflow
    - hadoop dfs -ls /top50ReferersToStephenHawking
    - hadoop dfs -ls /top50ReferersDonaldTrumph
    - hadoop dfs -ls /top50ReferersToPresidentialCandidates
    - hadoop dfs -ls /top50ReferersToObama
- Visualizations of Analysis have been shared in the repository at https://github.iu.edu/animhan/sw-project-template/blob/master/viz/
