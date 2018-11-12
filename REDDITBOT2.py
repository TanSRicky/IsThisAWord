import praw
import urbandictionary as ud
from psaw import PushshiftAPI
from nltk.corpus import wordnet as wn
from bs4 import BeautifulSoup
import bmemcached
import os

postIDs = {"0"}

api = PushshiftAPI()
mcLength = 0;
#client = swagger.ApiClient(os.environ('wnKEY'), os.environ('wnURL'))
mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
     os.environ.get('MEMCACHEDCLOUD_USERNAME'),
     os.environ.get('MEMCACHEDCLOUD_PASSWORD'))
mc.set("postIDs", postIDs)
reddit = praw.Reddit(client_id=os.environ['ID'],
                     client_secret=os.environ['SECRET'],
                     username=os.environ['REDDIT_USERNAME'],
                     user_agent= os.environ['useragent'],
                     passwordt=os.environ['REDDIT_PASSWORD'])
print(mc.get("initial"))
print(mc.get("hello"))
print("BEEP ABOVE")
      
if(mc.get("initial") == "0"):
    #mc.set("initial", "0")
    #mc.set("length", "0")
    #mc.set("temp", "0")
    print("beep initial")




def checkComments(ID):
    for i in range(0, mcLength):
        ID = mc.get(str(i))
        print(ID)
        if ID == subm.id:
            return False
        else:
            return True

def getPosts():
    mcIndex = int(mc.get("length"))
    print("beepy") 
    print(mc.get("0"))
    gen = api.search_comments(q='!IsThisAWord')
    for subm in gen:
        splitComment = subm.body.split(" ")
        word = ""
        if((splitComment[0] == "!IsThisAWord") and checkComments(subm.id)):
            for i in range(1,len(splitComment)):
                word += splitComment[i] + " "    
            word = word.strip()
            print("Bot replying to : ", subm.id)
            mc.set(str(mcIndex),subm.id)
            mcLength+=1
            print("Wrting..")
            try:        
                replyPosts(word,subm.id)
            except:
                print("maybe delted")
    mc.set("length",str(mcLength))   
            
   

def defUrban(word):
    print("beepy")
    try:
        defs = ud.define(word) 
        return defs[0].definition
    except:
        print("Whoops")
        pass
    try:
        r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(word))
        soup = BeautifulSoup(r.content)
        return soup.find("div",attrs={"class":"meaning"}).text
    except:
        return "I could not find that definition"

def defDict(word):
    try:
        wordApi = WordApi.WordApi(client)
        definitions = wordApi.getDefinitions(word)
        return definitions[0].text
    except:
        pass
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
        getPosts()
        print("Sleepy")

        
if __name__ == "__main__":
     print("beep")
     main()
           
