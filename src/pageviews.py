from pyspark.sql.functions import col
from pyspark.sql.functions import *
from pyspark.sql import SQLContext, Row
from pyspark import SparkContext, SparkConf

sc = SparkContext()
sqlContext = SQLContext(sc)

sc.setLogLevel("ERROR")
raw_data = sc.textFile("/wiki/pageviews-by-second-tsv")
header = raw_data.first()
data2 = raw_data.filter(lambda x:x!=header)
print "No of entries"
data2.count()

lines = data2
parts = lines.map(lambda l: l.split("\t"))
entries = parts.map(lambda p: Row(timestamp=p[0].replace('\"',''), site=p[1].replace('\"',''), requests=int(p[2])))

schemaEntries = sqlContext.createDataFrame(entries)
schemaEntries.registerTempTable("entries")

schemaEntries.printSchema()
print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
q1 = sqlContext.sql("SELECT * from entries")
q1.cache()
q1.sort("timestamp").show()
q1.orderBy("timestamp",col("site").desc()).show()
print "Sorted entries"
#q1.show(20, False)

print "------------------------------------------------------------------------------------------"
print "No of incoming requests in mobile vs desktop"
print "------------------------------------------------------------------------------------------"
q1.filter(col("site").like("%mobile%")).count()
q1.filter(col("site").like("%desktop%")).count()
q1.groupBy(col("site")).count().show()
q1.select(sum(col("requests"))).show()

print "------------------------------------------------------------------------------------------"
print "Sum of requests for Mobile viewers"
print "------------------------------------------------------------------------------------------"
q1_1 = q1.filter(col("site").like("%mobile%")).select(sum(col("requests"))).show()
print "Sum of requests for Desktop viewers"
q1_2 = q1.filter(col("site").like("%desktop%")).select(sum(col("requests"))).show()

print "------------------------------------------------------------------------------------------"
print "Converting to timestamp"
print "------------------------------------------------------------------------------------------"
q1v2 = q1.select(col("timestamp").cast("timestamp").alias("timestamp"),col("site"),col("requests"))
q1v2.cache()

print "------------------------------------------------------------------------------------------"
print "Analyzing how many diff years our data is from"
print "------------------------------------------------------------------------------------------"
q1v2.select(year(col("timestamp"))).distinct().show()

print "------------------------------------------------------------------------------------------"
print "Analyzing statistics of requests for mobile and desktop"
print "------------------------------------------------------------------------------------------"
q1v2.filter(col("site").like("%mobile%")).select(avg(col("requests")),min(col("requests")),max(col("requests"))).show()
q1v2.filter(col("site").like("%desktop%")).select(avg(col("requests")),min(col("requests")),max(col("requests"))).show()

print "------------------------------------------------------------------------------------------"
print "Which day of the week does wiki get most traffic?"
print "------------------------------------------------------------------------------------------"
q1v3 = q1v2.groupBy(date_format(col("timestamp"),"E").alias("Day of the week")).sum().cache()
#to visualize above by day of the week
q1v3.orderBy(col("Day of the week"))
q1v3.show()

#visualize both mobile and desktop requests in line chart
print "------------------------------------------------------------------------------------------"
print "Compare mobile and desktop requests by Day of the week"
print "------------------------------------------------------------------------------------------"
print "For mobile"
q1v4 = q1v2.filter(col("site").like("%mobile%")).groupBy(date_format(col("timestamp"),"E").alias("Day of the week")).sum().withColumnRenamed("sum(requests)","total_requests").select(col("Day of the week"),col("total_requests")).orderBy(col("Day of the week"))
q1v4.show(20,False)

print "For desktop"
q1v5 = q1v2.filter(col("site").like("%desktop%")).groupBy(date_format(col("timestamp"),"E").alias("Day of the week")).sum().withColumnRenamed("sum(requests)","total_requests").select(col("Day of the week"),col("total_requests")).orderBy(col("Day of the week"))
q1v5.show(20,False)
print "------------------------------------------------------------------------------------------"

