import tweepy 
import keys
from lyricsgenius import Genius
from rauth import OAuth1Service
import random

def tweet(api: tweepy.API, genius, song_num: int):
# This is the function that sends out the tweet containing a lyric (up to 240 characters) from a given musician/group (Juice WRLD by default) to social media website X

    # find artist ID (for other musicians change "Juice WRLD" to the name of the musician/group you are looking for)
    artist_id = genius.search_artists("Juice WRLD")['sections'][0]['hits'][0]['result']['id']
    #print(artist_id)
    page = 1000 # looks for songs within the top 1000 most popular for the given artist

    # gets the song ID of a song within the top 1000 most popular songs of an artist 
    random_id = 0
    while random_id == 0:
        try:
            random_id = genius.artist_songs(artist_id, per_page=1, page=random.randint(0, page), sort='popularity')['songs'][0]['id'] 
        except:
            print("Random number out of bounds")
    try:
        lyrics = genius.search_song(song_id=random_id, get_full_info=True) # obtain lyrics to song
    except:
        print("could not find song for song id = ", random_id)
        random_id = 0
        while random_id == 0:
            try:
                random_id = genius.artist_songs(artist_id, per_page=1, page=random.randint(0, page), sort='popularity')['songs'][0]['id'] 
            except:
                print("Random number out of bounds")

    lyrics = str(lyrics.lyrics) # convert lyrics to string and get just lyrics
    #print(lyrics)
    verses = []
    line = ""
    word = ""
    in_lyrics = False # a boolean value, used to remove non lyrical text commonly found on Genius, like "[Chorus]"
    for letter in lyrics:

        if letter == "[" or letter == "/": # "[" denotes the start of [chrous] for example. The "/" shows up followed by "205", or "2005" and is in the place of spaces, not sure why
            if letter == "[" and in_lyrics == True: # end of verse/chorus found
                verses.append(line)
                line = ""

            in_lyrics = False # do not include non lyrical text

        elif letter == "]" or letter == "5": # "]" denotes the end of [chrous] for example. The "5" shows up following "/20", or "/200" and is in the place of spaces, not sure why
            
            if letter == "5": # replace "/205", "/2005" with a space
                letter = " "
                in_lyrics = True # returned to lyrics
            
            else:
                in_lyrics = True # returned to lyrics
                continue


        if in_lyrics == True:
            if letter == "\n" or letter == " ": # new line or space denotes end of word
                
                if line == "": # word starts line
                    line += word
                    word = ""

                else: # line has pre-existing content
                    line += " "
                    line += word
                    #print(line)
                    word = ""

            else:
                word += letter # add letter to word
    # end of for loop

    try:
        num = random.randrange(1, len(verses), 1) # choose random verse
    except:
        print("presumably, song did not have a '[' anywhere in the set of lyrics", genius.search_song(song_id=random_id, get_full_info=True))
        num = 0
    tweet = str(verses[num])
    #print(tweet)
    if len(tweet) > 185: # check if tweet is over X character limit, very likely, leaves space for hashtags to increase viewability
        newtweet = ""
        line = ""
        for letter in tweet: # similar to what was done in the for loop
            #print(sentence)
            if letter != " ":
                line += letter
            else:
                if len(newtweet) + len(line) + 1 <= 185:
                    #print(len(str(newtweet)) + len(str(line)))
                    newtweet += " "
                    newtweet += line
                    line = ""

                else:
                    tweet = newtweet
                    break

    if tweet[-14:] == "You might also": # for some reason, "You might also like" shows up at the end of a verse / beginning of another verse, very strange, this accounts for that
        tweet = tweet[:-14]

    if tweet[:3] == "like": # for some reason, "You might also like" shows up at the end of a verse / beginning of another verse, very strange, this accounts for that
        tweet = tweet[4:]

    if tweet[:5] == "Lyrics":
        tweet = tweet[5:]

    tweet += " #JuiceWRLD #LLJW #LND #DRFL #GBGR #Unreleased #TPNE"
    
    #print(tweet)

    post_result = newapi.create_tweet(text=tweet) # post tweet

    file = open("tweet_IDs.txt", "a") # a list of all post IDs is made, such that they can be deleted easily
    file.write(post_result[0]["id"]) # obtains post ID from value returned 
    file.write("\n")
    file.close()
    
    # How to delete a post using the post ID shown below
    #post_delete = newapi.delete_tweet(post_result[0]["id"])
    
    #print('tweeted')
    print(post_result)
    #print(post_delete)


if __name__ == '__main__':
    
    # Gain access to the twitter API through tweepy, you can get your own key via https://developer.twitter.com/en/portal/
    newapi = tweepy.Client(
        bearer_token=keys.bearer_token_twit,
        access_token=keys.access_token_twit,
        access_token_secret=keys.access_token_secret_twit,
        consumer_key=keys.api_key_twit,
        consumer_secret=keys.api_secret_twit,
    )
    genius = Genius(keys.access_token_genius) # gain access to the genius API, key via https://docs.genius.com/
    num = random.randrange(1, 1000, 1) # pick a number for the song on the musician/group top 1000 most popular
    tweet(newapi, genius, num) # function call for the tweet to be made and sent