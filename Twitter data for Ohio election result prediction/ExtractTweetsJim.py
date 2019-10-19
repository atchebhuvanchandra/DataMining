
import tweepy
import jsonpickle
ckey='9o4nF1838xVjdzRfHLsyxBHT9'
csecret='PzO48f0Cbxv4rjw1W5XMAmJHxOKM0bITMK10w1nwh0XX3y26Fz'
atoken='1066920280168296448-e130jGigt8X89LWZjBodsDBxMiCGKP'
asecret='Z8pqbjTWJ4wtyb7vcd0mvBNUFDjqszCKNqmQhSHJQYK3a'

auth=tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api = tweepy.API(auth,wait_on_rate_limit=True)
count = 0
file=open('/Users/ramnarayan/Desktop/twitterdata/OhioSenate2_new.json','a')
for tweet in tweepy.Cursor(api.search,q="#JimRenacci OR #OhioSen OR #OhioPrimary OR @Repjimrenacci",lang="en").items():
	file.write(jsonpickle.encode(tweet._json,unpicklable=False) +'\n')
	count= count +1
print("total count",count)	


