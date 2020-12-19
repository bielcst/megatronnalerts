from riotwatcher import RiotWatcher, ApiError
import time
import tweepy
import atexit

def save():
	file = open("number.txt","w")
	file.write(str(number))
	file.close()

atexit.register(save)
#setting api things up
consumer_key = 'twitter_consumer_key'
consumer_secret = 'twitter_consumer_secret'
access_token = 'twitter_access_token'
access_token_secret = 'twitter_secret_access_token'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

watcher = RiotWatcher('riot_api_key')
criminoso = watcher.summoner.by_name('br1', 'megatronn')
mensagem1 = 'Megatronn está jogando, coloque na fila antes do jogo dele acabar.'
mensagem2 = 'O jogo do Megatronn acabou agora, cuidado ao entrar na fila.'

#opening the tweet number
file = open("number.txt","r") 
number = int(file.read())
file.close()

while True:
    last_tweet = api.user_timeline(screen_name = 'AlertsMegatronn', count =1)[0]    
    try:
        ingame = watcher.spectator.by_summoner('br1', criminoso['id'])
    except:
        ingame = ''
        if last_tweet.text == mensagem1 + str(number) and bool(ingame) == False:
            number = number + 1
            api.update_status(mensagem2 + str(number))
    if last_tweet.text == mensagem2 + str(number):
        if ingame:
            number = number + 1
            api.update_status(mensagem1 + str(number))
            

    time.sleep(60)
