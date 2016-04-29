================
Project Proposal
================
==================================================
Exploratory Data Analysis of English Wikipedia
==================================================

******
Team
******
1. Ashwin Nimhan, animhan@indiana.edu, animhan, animhan
2. Manashree Rao, manarao@indiana.edu, manarao, Manashree

******
Roles
******
1. Deployment - Ashwin and Manashree
2. Configuration - Manashree
3. Algorithm - Ashwin and Manashree
4. Analytics - Ashwin and Manashree
5. Visualization - Ashwin

**********
Artifacts
**********
- Ansible roles for deployment of Spark, HDFS, YARN.
- Analytics scripts on Spark

******************************
List of Technologies
******************************
Development Languages
---------------------
- Python
- Javascript
- Java

Software Tools
---------------------
- Ansible
- Apache Spark
- MLlib
- GraphX
- SparkSQL
- Spark Streaming
- NodeJS
- MongoDB
- Nginx
- D3.js
- Mesos
- Parquet

Compute Resources
---------------------
- OpenStack in FutureSystems

System Requirements
---------------------
- Size: 12 VM instances with m1.medium 
- OS: Ubuntu 14.04 LTS
- Storage: 480GB

List of DataSets
---------------------
- English Wikipedia data dump latest (https://dumps.wikimedia.org/enwiki/)
- English Wikipedia pageviews by second (https://datahub.io/dataset/english-wikipedia-pageviews-by-second)
- Wikipedia Clickstream: March 2016 (https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/4901611/2016_03_clickstream.tsv.gz)
- Live Edit Stream for English Wikipedia (socket listening to stream.wikimedia.org/rc)
- Other supporting datasets as required for enrichment (https://datahub.io/organization/wikimedia)

Schedule
-----------
- Week 1: Initial Meeting
- Week 2: Proposal
- Week 3: Discussion
- Week 4: Presentation
- Week 5: Process data into required format
- Week 6: Build systems
- Week 7: Develop modules, test run
- Week 8: Final Report, Review, Submission

Project Style and Type
-----------------------
- Bonus
- Deployment
  -  Setup of Spark, HDFS and YARN using Ansible scripts.
- Analytics
  -  Analyzing English Wikipedia Data to derive insights using the above framework.


Acknowledgement
---------------------
- https://datahub.io/organization/wikimedia
- Spark tutorials online
