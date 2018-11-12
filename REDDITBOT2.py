import praw
import urbandictionary as ud
from psaw import PushshiftAPI
from nltk.corpus import wordnet as wn
from bs4 import BeautifulSoup
import bmemcached



#client = swagger.ApiClient(os.environ('wnKEY'), os.environ('wnURL'))
mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
     os.environ.get('MEMCACHEDCLOUD_USERNAME'),
     os.environ.get('MEMCACHEDCLOUD_PASSWORD'))

reddit = praw.Reddit(os.environ['ID'],
                     os.environ['SECRET'],
                     os.environ['REDDIT_PASSWORD'],
                     os.environ['useragent'],
                     os.environ['REDDIT_USERNAME'])

api = PushshiftAPI()
mcLength = 0
mcIndex = 0
def checkComments(ID):
    for i in range(0, mcLength):
        ID = mc.get(str(i))
        if ID == sumb.id:
            return False
        else:
            return True

def getPosts():
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
            
   

def defUrban(word):
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
        time.sleep(30)
        
if __name__ == "__main__":
     print("beep")
     main()
           
