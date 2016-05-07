Visualization of Data
=====================

- The output from spark scripts is stored in HDFS. The following command is used to extract required columns using Linux CLI utility and export as csv:
 hadoop fs -cat /topReferersToStephenHawking/part-00000 | awk -F"," '{ print $5","$2","$3 }' > temp.csv; sed -i '1isource,target,value' temp.csv
- This command can be modified to extract entries as required from different output files stored in HDFS.
- Basic visualization like Bar, Pie and Line chart have been visualized using Excel; Html, CSS, d3.js have been used to create the sankey diagram.
