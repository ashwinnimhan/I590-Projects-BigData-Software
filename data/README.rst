
=====================================================
Exploratory Data Analysis of English Wikipedia - Data
=====================================================
Sample Datasets have been added to this folder.

List of Original DataSets
-------------------------
- English Wikipedia pageviews by second (https://ckannet-storage.commondatastorage.googleapis.com/2015-04-26T22:07:22.853Z/pageviews-by-second-tsv.gz) (263MB)
- Wikipedia Clickstream: Feb 2015 (https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/5036383/2015_02_en_clickstream.tsv.gz) (1.2GB)

Clickstream metadata
---------------------
The data includes the following 6 fields:
    1. prev id: referrer id
    2. curr id: the unique MediaWiki page ID of the article the client requested
    3. n: the number of occurrences of the (referrer,resource) pair
    4. prev title: referrer URL
    5. curr title the title of the article the client requested
    6. type of link: can be empty/missing, external link or internal wiki link

Pageviews Data
---------------
This file contains a count of pageviews to the English-language Wikipedia:
    1. requests: Count of pageviews
    2. site: mobile or desktop
    3. timestamp: timestamp of pageviews

After analyzing the data:

For top 50 wiki articles: 
    - Field 1: Article title (curr_title in original data)
    - Field 2: Request count (sum of requests(n) in original data)

For top 50 requested pages that are missing: 
    - Field 1: Article title (curr_title in original data with link = redlink(missing))
    - Field 2: Request count (sum of requests(n) in original data)

For top 25 articles referred from twitter(trending on social media): 
    - Field 1: Article title (curr_title in original data)
    - Field 2: Request count (sum of requests(n) in original data)

For top 50 wiki articles: 
    - Field 1: Article title (curr_title in original data)
    - Field 2: Request count (sum of requests(n) in original data)

For all other outputs that map referrer of the article used in sankey visualization ie., sankey-ReferersToStephenHawking.csv, sankey-bernie-sanders.csv, sankey-clinton.csv, sankey-cruz.csv, sankey-obama.csv:
     - source: maps to prev_title in original data
     - target: maps to curr_title in original data
     - value: maps to sum of requests i.e., 'n' in original data

For identifying traffic inflow vs outflow for most requested pages: 
    - Field 1: Article title (curr_title in original data)
    - Field 2: in_count (sum of requests(n) where field 1 is "curr_title" in original data)
    - Field 3: out_count (sum of requests(n) where field 1 is "prev_title" i.e., referrer in original data)
    - Field 4: ratio of field 1 and 2
    
Other details about the data can be found in the project report uploaded to the repository
