import magic
from bot.Items import *
import random
import time
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from pytube import YouTube
import uuid
import csv
from bot.Constants import *
import os
import youtube_dl




class get_videos() :
    keywords=list()
    videos=list()

    def __init__(self) -> None:
        
        self.driver=Driver(headless=True )

    def input_select_user (self) :
        print('These are your current Accounts :')
        for elem in USERS_LIST:
            print(elem)
        while True:
            i = input("Choose Username From the List : ")
            for elem in USERS_LIST:
                if elem.username.upper() == i.upper():
                    print(f'{elem} selected ')
                    return elem
            else:
                print('Invalid Username, Choose from The List : \n')


    def get_input(self) :
        while True : 
            keyword= input('Type Keyword , STOP to end input :\n')
            if keyword.upper() == 'stop'.upper() :
                log(f'Processing {len(self.keywords)} inputs : ')
                for e in self.keywords : 
                                log(e)
                break
            else :
                user=self.input_select_user()
                n=input(f'Type number of Youtube videos for {keyword} , R to randomise ({RANDOM_MIN},{RANDOM_MAX})\n')
                if n.upper()== 'r'.upper()  : 
                    num=random.randint(1,10)
                else : 
                    num=int(n)
                if USE_DEFAULT_VIDEO_LIMITS == False :
                    max,min=self.input_video_limit()
                else : 
                    max=DEFAULT_MAX
                    min=DEFAULT_MIN
                self.keywords.append(KeywordItem(keyword,num,max,min,user))
                


    def input_video_limit(self) :
        while True :
            i=input(f'Use default Youtube video limits ({DEFAULT_MIN}-{DEFAULT_MAX}) y/n ? : \n')
            if i.upper()=='y'.upper() :
                return DEFAULT_MAX,DEFAULT_MIN
            elif i.upper()=='n'.upper(): 
                max=input('Type maximum length for youtube videos (in minutes) : \n')
                min=input('Type minimum length for youtube videos (in minutes) : \n')
                return max,min
            else :
                print('Wrong awnser , type y for yes or n for no \n')
                
                    
                
        

    def check_length(self,elem,min,max) : 
        T = [int(i) for i in str(elem).split() if i.isdigit()]
        if elem is None or str(elem) == "Shorts":
            return True
        elif str(elem).__contains__("houres") or str(elem).__contains__('hour')  :
            if str(elem).__contains__('minutes') or str(elem).__contains__('minute') :
                if (int(T[0])*60 + int(T[1])) < min :
                    return True
                if (int(T[0])*60 + int(T[1])) > max :
                    return True
            else :
                if (int(T[0])*60 ) <min :
                    return True
                if (int(T[0])*60 ) >max :
                    return True
        elif not str(elem).__contains__('minutes') :
                return True
        elif T[0] < min : 
                return True
        elif T[0] > max : 
                return True
        return False
                
    def search(self) :
            self.videos.clear()
            for elem in self.keywords : 
                log(f'Getting Youtube Videos for Keyword : {elem.Keyword}')
                self.driver.get(f'https://www.youtube.com/results?search_query={elem.Keyword}')
                time.sleep(5)
                start_time=time.time()
                while True :
                    self.driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
                    time.sleep(2)
                    list=self.driver.find_elements(By.TAG_NAME,'ytd-video-renderer')
                    for elm in list : 
                        Title = elm.find_element(By.ID ,'video-title').get_attribute('title')
                        Link = elm.find_element(By.CLASS_NAME,'yt-simple-endpoint').get_attribute('href')
                        Length = elm.find_element(By.ID,'text').get_attribute('aria-label')
                        #print(Length)
                        #if self.check_length(Length,elem.min_length,max_length) :
                            #continue
                        id=uuid.uuid4()
                        self.videos.append(videoItem(id,Title,Link,Length,elem))
                        #print(len(self.videos))
                        if len(self.videos) == int(elem.num_of_videos) : 
                            log(f'Search over , {len(self.videos)} videos : ')
                            for e in self.videos : 
                                log(e)
                            return self.videos
                        if time.time()>=start_time+SEARCH_TIMEOUT :
                            log(f"Search time limit exceeded , {len(self.videos)} videos : ")
                            for e in self.videos : 
                                log(e)
                            return self.videos
                    self.videos.clear()
    
    def Isvideo(self,file) :
        mime = magic.Magic(mime=True)
        filename = mime.from_file(file)
        if filename.find('video') != -1:
            return True
        else :  
            return False

    
    def download_videos(self) :
        for elem in self.videos:
            flist=os.listdir(DOWNLOAD_PATH)
            try :
                log(f'Downloading {elem.title} ')
                try :
                    YouTube(str(elem.link),use_oauth=True,allow_oauth_cache=True).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(DOWNLOAD_PATH,filename_prefix=f'{str(elem.id)}====')
                except :
                    ydl_opts = {'outtmpl': f'{DOWNLOAD_PATH}\===={elem.id}.mp4'}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([elem.link]) 
                while True :
                    verif=False
                    new_flist=os.listdir(DOWNLOAD_PATH)
                    if len(new_flist) > len(flist) :
                        new_file=new_flist[0]
                        if self.Isvideo(f'{DOWNLOAD_PATH}\{new_file}') == True :
                            log('Donwload completed')
                            os.replace(f'{DOWNLOAD_PATH}\{new_file}',f'{READY_TO_TREAT_PATH}\{new_file}')
                            verif=True
                            break
                        else :
                            log('Corrupt or bad format file detected , deleting .. ')
                            os.remove(f'{DOWNLOAD_PATH}\{new_file}')
                            break
                if verif :
                    with open('id.csv','a',newline='',encoding='utf-8') as f :
                        writer = csv.writer(f)
                        writer.writerow([elem.id,elem.Keyword.user.session_id])
            except :
                log('Could not download video , skiping..') 
        os.mkdir(f'{DOWNLOAD_PATH}\_finished')
        log('NO MORE VIDEOS TO DOWNLOAD..')

    


    def get_videos(self) : 
        return self.videos
    def get_keywods(self) :
        return self.keywords