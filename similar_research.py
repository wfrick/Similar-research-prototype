import pandas as pd
from utilities import *

#NEXT STEPS
#1. save everything to CSV so no repeats
#2. assign to nearest editor
#3. expand beyond headlines, to include abstracts


#Import headlines, stem and remove stopwords, and group by topic
heds = pd.read_csv("headlines.csv",encoding='utf-8')
tk = heds_to_topics(heds)
#Topics is a list of topic names; beats is a list of stemmed text
topics = tk[0]
beats = tk[1]

#For a given RSS feed, get items similar to headlines
feed = 'https://qz.com/feed'
parse_similarity(feed,topics,beats)


'''
#Research feeds
nber = 'http://www.nber.org/rss/new.xml'
management_science = 'https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=mnsc'
eureka = 'https://www.eurekalert.org/rss/business.xml'
pnas = 'http://feeds.feedburner.com/pnas/SMZM'
'''

'''
#Media
nyt = 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
atlantic = 'https://www.theatlantic.com/feed/all/'
economist = 'http://www.economist.com/sections/business-finance/rss.xml'
techreview = 'https://www.technologyreview.com/stories.rss'
washpost = 'http://feeds.washingtonpost.com/rss/business'
qz = 'https://qz.com/feed'
vox = 'https://www.vox.com/rss/index.xml'
mckinsey = 'https://www.mckinsey.com/insights/rss.aspx'
conversation = 'https://theconversation.com/us/articles.atom'
hbr = 'http://feeds.hbr.org/harvardbusiness/'
'''
