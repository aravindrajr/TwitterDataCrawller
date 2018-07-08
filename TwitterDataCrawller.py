# -*- coding: utf-8 -*-
"""
Created 

@author: Aravind Raj R
"""

'''   You need to login to twitter from your browser before ,for code  work 
        it doesnot automate the login process yet
'''

import progressbar
import time,os

import json,requests
from bs4 import BeautifulSoup


def getInitialPage(topic):
    url = "https://twitter.com/search?q={0}&src=typd".format(topic)
    with open("headers.json", 'r') as fileContents:
        jsonRaw = json.loads(fileContents.read())
    #Build dict from json
    headers = {}
    for item in jsonRaw['headers']:
        headers[item['name']] = item['value']
        
    r = requests.get(url ,headers = headers)
    writeResponseToTextFile(r.text.encode('utf-8'))
    return r.text
        
def writeResponseToTextFile(text):
    with open("pageContent.txt", 'w') as fileContents:
        fileContents.write(text)
    with open("pageContent.html", 'w') as fileContents:
        fileContents.write(text)

def readResponseFromTextFile():
    with open("pageContent.txt", 'r') as fileContents:
        temp = fileContents.read().decode('utf-8')
    if temp:
        return temp
    return None

def getTweetData(htmlContent):
    ExtractedData = []
    
    soup = BeautifulSoup(htmlContent,"lxml")
    for i in soup.find_all("div", {"class":"tweet"}):
        tweetData = {}

        if i.find('span',{'class':'ProfileTweet-actionCount'}):
            temp = i.find('span',{'class':'ProfileTweet-actionCount'}).text.encode('utf-8').lstrip().rstrip() #replies
            tweetData['replies'] = temp[0:temp.index('r')-1] 
        else:
            tweetData['replies'] = '0'

        if i.find('span',{'class':'ProfileTweet-action--retweet'}):
            temp = i.find('span',{'class':'ProfileTweet-action--retweet'}).text.encode('utf-8').lstrip().rstrip() # retweets
            tweetData['retweets'] = temp[0:temp.index('r')-1] 
        else:
            tweetData['retweets'] = '0'

        if i.find('span',{'class':'ProfileTweet-action--favorite'}):
            temp =  i.find('span',{'class':'ProfileTweet-action--favorite'}).text.encode('utf-8').lstrip().rstrip() #likes
            tweetData['likes'] = temp[0:temp.index('l')-1] 
        else:
            tweetData['likes'] = '0'

        if i.find('span',{'class':'username'}):
            tweetData['handle'] = i.find('span',{'class':'username'}).text.encode('utf-8').lstrip().rstrip() #twitter Handle
        else:
            tweetData['handle'] = 'Unknown'
        
        if i.find('p', {'class':'TweetTextSize'}):
            tweetData['tweet'] = i.find('p', {'class':'TweetTextSize'}).text.encode('utf-8').lstrip().rstrip() # Tweet
        else:
            tweetData['tweet'] = ''
        ExtractedData.append(tweetData)
    return ExtractedData

def main():
    getInitialPage("trump")
    htmlText = readResponseFromTextFile()
    tweets = []
    if htmlText :
        tweets += getTweetData(htmlText)
    
    print len(tweets)
    print "\n--------------------------------------------------------------\n"
    for i in tweets:
        print i 
        print ""
    #for i in progressbar.progressbar(range(100)):
    #    s=1+1

main()

    







'''
                        #template for reload
        RELOAD_URL = "https://twitter.com/i/search/timeline?f=tweets&vertical=" \
                     "default&include_available_features=1&include_entities=1&" \
                     "reset_error_state=false&src=typd&max_position={pos}&q={q}"
        

            for tweet  in soup2.find_all("div", {"class":"content"}):
                temp1= tweet.find("a",{"class":"tweet-timestamp"}).get("title")
                [s.extract() for s in tweet('a')]
                if tweet.find("p",{"class":"TweetTextSize js-tweet-text tweet-text"}):
                    if tweet.find("p",{"class":"TweetTextSize js-tweet-text tweet-text"}).get("lang") == "en":
                        temp2= tweet.find("p",{"class":"TweetTextSize js-tweet-text tweet-text"}).text
                all_tweets[temp2]=temp1
'''