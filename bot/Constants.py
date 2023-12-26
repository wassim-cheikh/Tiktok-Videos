from bot.Items import *
import logging
DOWNLOAD_PATH=""
READY_PATH=""
TREATING_PATH=""
API_KEY = "open ai api key"
EXAMP=' {"start": 893.04, "end": 903.12, "transcript": "the new best league of legends companion app with so many new features, its a huge improvement from anything I have used in the past and I highly recommend you download it for free from the link in the description, thanks so much for watching!", "score": 4},'
def SCORE_PROMPT(elem) :
    return f"the following data is a timestamped transcript of a youtube video Please merge successive elements that are sense related or it's the same sentence or you think it shouldn't be splitted ,after you merge , give each element a score from 0 to 10 based on this scoring system : [if you think this part is worth to be uploaded on tiktok = from 0 to 2 points,if there is something interesting hapening = from 0 to 2 points,if there is something funny or weired happening = from 0 to 2 points,if there is expressing of feelings , happiness , anger,laughter,crying... = from 0 to 2 points] each line of the output should in json format , strictly follow this example : {EXAMP}. this is the data :  \n {elem}] "
def CAPTION_PROMPT (transcript) :
    return f"i need you to generate one good title with 3 viral hashtags for a tiktok video having this transcript : {transcript} "
def log (message) : 
    logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",format="%(asctime)s %(levelname)s %(message)s")
    logging.info(message)
    print(message)

USERS_LIST=[userItem('tiktok username','tiktok session id')]
USE_DEFAULT_VIDEO_LIMITS=False
DEFAULT_MAX=20
DEFAULT_MIN=3
READY_TO_TREAT_PATH=""
MINIMUM_SCORE=3
SHORTS_MINIMUM_LENGTH=30
SHORTS_MAXIMUM_LENGTH=240
MAXIMUM_NUMBER_OF_SHORTS=5
SEARCH_TIMEOUT=420
RANDOM_MAX=1
RANDOM_MIN=10
CROP_SIZE=9/16