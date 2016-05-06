from pyspark.sql.functions import col
from pyspark.sql.functions import *
from pyspark.sql import SQLContext, Row

from pyspark import SparkContext, SparkConf

import re

def toCSVLine(data):
  return ','.join(str(d) for d in data)

sc = SparkContext()
sqlContext = SQLContext(sc)
sc.setLogLevel("ERROR")
raw_data = sc.textFile("/wiki/2015_02_en_clickstream.tsv")
header = raw_data.first()
data2 = raw_data.filter(lambda x : x != header)     
data2.count()

lines = data2
parts = lines.map(lambda l: l.split("\t"))
entries = parts.map(lambda p: Row(prev_id=re.sub(r'[^\x00-\x7F]+','',p[0]), curr_id=re.sub(r'[^\x00-\x7F]+','',p[1]), no = re.sub(r'[^\x00-\x7F]+','',p[2]),prev_title=re.sub(r'[^\x00-\x7F]+','',p[3]), curr_title=re.sub(r'[^\x00-\x7F]+','',p[4]), typeOf =re.sub(r'[^\x00-\x7F]+','',p[5])))

schemaEntries = sqlContext.createDataFrame(entries)
schemaEntries.registerTempTable("entries")

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
schemaEntries.printSchema()
schemaEntries.show()

q1 = sqlContext.sql("SELECT * from entries").cache()
q1.registerTempTable("topEntries")
q2= q1.select(col("prev_title"),col("curr_title"),col("no").cast("Int").alias("no"),col("typeOf")).cache()

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Top articles ..... "
print "Writing query for top 10 wiki articles in sparkSQL to wiki to HDFS. Displaying top 10 ........"
q3 = q2.groupBy(col("curr_title")).sum().select(col("curr_title"),col("sum(no)")).orderBy(col("sum(no)").desc()).limit(50)
q3 = q2.groupBy(col("curr_title"))
q4 = q3.sum().select(col("curr_title"),col("sum(no)")).orderBy(col("sum(no)").desc())
q4.show(10, False)
lines = q4.map(toCSVLine)
lines.saveAsTextFile('/top50WikiArticles')

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Top Referers .... "
print "Writing query for Top 50 Referers to wiki to HDFS. Displaying only top 10 ........"
q6 = q2.groupBy(col("prev_title")).sum().orderBy(col("sum(no)").desc()).limit(50)
q6.show(10, False)
lines = q6.map(toCSVLine)
lines.saveAsTextFile('/top50Referers')

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Trending on Social Media .... "
print "Writing query for Top 50 trending articles in twitter in feb 2015 to HDFS. Displaying only top 5 ........"
q7_1 = q2.filter(col("prev_title").like("%other-twitter%")).groupBy(col("curr_title"))
q7_2 = q7_1.sum().orderBy(col("sum(no)").desc()).limit(5)
q7_2.show()

q7_3 = sqlContext.sql("SELECT curr_title,SUM(no) AS top_twitter FROM topEntries WHERE prev_title = 'other-twitter' GROUP BY curr_title ORDER BY top_twitter DESC limit 50")
lines = q7_3.map(toCSVLine)
lines.saveAsTextFile('/top50TrendingOnTwitter')

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Different types of links in Wikipedia - "
q8_0 = sqlContext.sql("SELECT DISTINCT typeOf from topEntries")
q8_0.show()

print "Most Requested Missing Pages"
print "Writing query for Top 50 missing pages to HDFS. Displaying only top 5 ........"
q8_1 = q2.filter(col("typeOf").like("%redlink%")).groupBy(col("curr_title"))
q8_2 = q8_1.sum().orderBy(col("sum(no)").desc()).limit(50)
q8_2.show(5,False)
lines = q8_2.map(toCSVLine)
lines.saveAsTextFile('/top50RequestedMissingPages')

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Inflow vs Outflow"
print "Pageviews per article"
pageViewsPerArticle = q2.groupBy(col("curr_title")).sum().withColumnRenamed("sum(no)","in_count").cache()
pageViewsPerArticle.show(10, False)

print "Link clicks per article"
linkClicksPerArticle = q2.groupBy(col("prev_title")).sum().withColumnRenamed("sum(no)","out_count").cache()
linkClicksPerArticle.show(10,False)

print "Writing query for Inflow vs Outflow for Top 50 Most requested pages."
in_outDF = pageViewsPerArticle.join(linkClicksPerArticle,(col("curr_title") == col("prev_title"))).orderBy(col("in_count").desc())

lines = in_outDF.map(toCSVLine)
lines.saveAsTextFile('/top50InflowVsOutflow')

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Ratio of inflow to outflow: if a person clicks on x, how many continue from there"
ratio = in_outDF.withColumn("ratio",col("out_count")/col("in_count")).cache()
ratio.show(5,False)

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Traffic flow pattern for a specific article - Stephen Hawking"
ratio.filter(col("curr_title").like("%Stephen_Hawking%")).show()

print "Which referers send most traffic to Stephen Hawking article"
q9 = sqlContext.sql("SELECT * FROM topEntries WHERE curr_title LIKE 'Stephen_Hawking' ORDER BY no DESC LIMIT 10")
q9.show()
lines = q9.map(toCSVLine)
lines.saveAsTextFile('/topReferersToStephenHawking')

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "What percent of page visits are from wikipedia itself?"
q10_1 = q2.filter(col("prev_title").like("%other-wikipedia%")).groupBy(col("curr_title"))
q10_2 = q10_1.sum().orderBy(col("sum(no)").desc())
totalclicks = q1.count()
wikiclicks = q10_2.count()
vr = wikiclicks*100.0/totalclicks
print("Percentage of page visits in Wikipedia from other pages in Wikipedia itself: ",vr)

print "------------------------------------------------------------------------------------------"
print "------------------------------------------------------------------------------------------"
print "Top referrers to Donald Trump"
q11_0 = sqlContext.sql("SELECT * FROM entries WHERE curr_title = 'Donald_Trump' AND prev_id IS NOT NULL AND prev_title != 'Main_Page' ORDER BY no DESC limit 50")
q11_01 = q11_0.show(10, False)
lines = q11_0.map(toCSVLine)
lines.saveAsTextFile('/topReferersToDonaldTrumph')

print "Top referrers to all presidential candidate pages"
q11_2 = sqlContext.sql("SELECT * FROM entries WHERE curr_title IN ('Donald_Trump', 'Bernie_Sanders', 'Hillary_Rodham_Clinton', 'Ted_Cruz') AND prev_id IS NOT NULL AND prev_title != 'Main_Page' ORDER BY no DESC limit 100")
q11_20 = q11_2.show(10, False)
lines = q11_2.map(toCSVLine)
lines.saveAsTextFile('/topReferersToPresidentialCandidates')

print "Top referrers to Barack Obama"
q11_1 = sqlContext.sql("SELECT * FROM entries WHERE curr_title = 'Barack_Obama' AND prev_id IS NOT NULL AND prev_title != 'Main_Page' ORDER BY no DESC limit 100")
q11_10 = q11_1.show(10, False)
lines = q11_1.map(toCSVLine)
lines.saveAsTextFile('/topReferersToObama')
