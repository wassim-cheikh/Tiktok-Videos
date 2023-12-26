import os
from bot.Constants import *
from bot.tiktok import uploadVideo
import time
import re
from bot.Items import *
import json
class upload_videos() :
    csvlist=list()
    users=list()
    def __init__(self) -> None:
        while True : 
            for elem in os.listdir(READY_PATH) :
                with open (f'{READY_PATH}\{elem}','r',encoding='utf-8') as f :
                    data = json.load(f)
                exist=self.check_user(data['user'])
                if  exist == None :
                    try:
                        uploadVideo(data['user'],data['file'],data['caption'],data['tags'])
                        self.users.append([data['user'],time.time()])
                        os.remove(f'{READY_PATH}\{elem}')
                        time.sleep(10)
                    except :
                        time.sleep(3600)
                        uploadVideo(data['user'],data['file'],data['caption'],data['tags'])
                        self.users.append([data['user'],time.time()])
                        os.remove(f'{READY_PATH}\{elem}')
                        time.sleep(10)
                else : 
                    continue
                for elem in os.listdir(READY_PATH) :
                    with open (f'{READY_PATH}\{elem}','r',encoding='utf-8') as f :
                        data = json.load(f)
                    exist=self.check_user(data['user'])
                    if  exist == None :
                        pass
                    else : 
                        log(f'Download Scheduled in {sleep} ')
                        sleep=time.time()+7200-exist[1]
                    uploadVideo(data['user'],data['file'],data['caption'],data['tags'])
                    self.users.append([data['user'],time.time()])
                    os.remove(f'{READY_PATH}\{elem}')
            files=os.listdir(f'{READY_PATH}')
            if len(files)==1 and files[0]=='_finished':
                self.clean()
                log('UPLOADED ALL VIDEOS .. STOPPING THE PROGRAM .')
                break

    def extract_dict(self,string) :
        results = []
        s_ = ' '.join(string.split('\n')).strip()
        exp = re.compile(r'(\{.*?\})')
        for i in exp.findall(s_):
            try:
                results.append(json.loads(i))        
            except json.JSONDecodeError:
                pass    
        return results

    def check_user(self,user) :
        if len(self.users)==0 :
            return None
        for elem in self.users :
            if  user == elem[0] :
                return elem
        return None


    def clean(self) :
        log('Removing Used Files')
        for elem in os.listdir(TREATING_PATH) :
            os.remove(f'{TREATING_PATH}\{elem}')
        for elem in os.listdir(DOWNLOAD_PATH) :
            os.remove(f'{DOWNLOAD_PATH}\{elem}')
        for elem in os.listdir(READY_TO_TREAT_PATH) :
            os.remove(f'{READY_TO_TREAT_PATH}\{elem}')
        for elem in os.listdir(READY_PATH) :
            os.remove(f'{READY_PATH}\{elem}')
        os.remove('id.csv')
        
        

   

                
                    
    