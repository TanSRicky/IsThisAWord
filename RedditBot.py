import praw
import pdb
import re
import os
import time
import urbandictionary as ud
from psaw import PushshiftAPI
from urllib.parse import quote_plus
from PyDictionary import PyDictionary
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from bs4 import BeautifulSoup


dictionary = PyDictionary()
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("test")
api = PushshiftAPI()



       
counter = 0;
#if re.search("test", submission.title, re.IGNORECASE):
                                #prints split comment

def getPosts():
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
           posts_replied_to = f.read()
           posts_replied_to = posts_replied_to.split("\n")
           posts_replied_to = list(filter(None, posts_replied_to))
    gen = api.search_comments(q='!IsThisAWord')
    max_response_cache = 5000000
    cache = []

    
    for subm in gen:
        splitComment = subm.body.split(" ")
        word = ""
        if((splitComment[0] == "!IsThisAWord") and (subm.id not in posts_replied_to)):
            for i in range(1,len(splitComment)):
                word += splitComment[i] + " "    
            word = word.strip()
            print("Bot replying to : ", subm.id)
            posts_replied_to.append(subm.id)
            print("Wrting..")
            with open("posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + "\n")
            try:        
                replyPosts(word,subm.id)
            except:
                print("maybe delted")
            
   

def defUrban(word):
      try:
          defs = ud.define(word) 
          return defs[0].definition
      except:
          print("Whoops")
          return "Could not find!"

def defDict(word):
        try:
            return wn.synsets(word.strip())[0].definition()
        except:
            return "Whoops!"
                

def replyPosts(word, commId):
    print("Beep beep")
    print("Found")
    def1 = defUrban(word)
    def2 = defDict(word)
    wordSearched = "__Defined:__ " + word
    replyText1 =  ("\n\n__Urban Dictionary:__ \n\n" + def1)
    replyText2 = ("\n\n__Regular Dictionary:__\n\n" + def2)
    botFooter = ("\n\n***\n\n")
    botFooter2= ("_I am a reddit bot._")
    reply = (wordSearched+""+replyText1+""+replyText2+""+botFooter+""+botFooter2)
    comment = reddit.comment(commId)
    comment.reply(reply)
    time.sleep(5)

def main():
    while 1 == 1:
        getPosts()
        print("Sleepy")
        time.sleep(30)
        
if __name__ == "__main__":
     print("beep")
     main()
