from pydub import AudioSegment
import os
from bot.Items import *
from bot.Constants import *
import time
import textwrap
import openai
import whisper
import json 
import re
from moviepy.editor import *
from moviepy.video.fx.all import crop
import magic
import uuid
import csv

class edit_videos() :
    def __init__(self) -> None:
        while True :
            files=os.listdir(READY_TO_TREAT_PATH)
            if len(files)>0 :
                file=files[0]
                log(f'New Download detected : {file} , generating audio... ')
                self.extract_audio(file)
                id=file.split('====')[0]
                os.replace(f'{READY_TO_TREAT_PATH}\{file}',f"{TREATING_PATH}\{id}\{file}")
            for id in os.listdir(TREATING_PATH) : 
                if  f'{id}.txt' not in os.listdir(f"{TREATING_PATH}\{id}") :
                    log(f'Generating transcript for {id}')
                    self.extract_transcript(f'{TREATING_PATH}\{id}\{id}.wav',f'{TREATING_PATH}\{id}\{id}.txt')
                if  f'{id}.csv' not in os.listdir(f"{TREATING_PATH}\{id}") :
                    log(f'Generating scores for : {id}')
                    self.score(id)
                files=os.listdir(f'{TREATING_PATH}\{id}')
                if 'shorts' not in files and f'{id}.csv' in files :
                        log(f'Generating shorts for : {id}')
                        self.extract_videos(self.extract_csv(id),id)
            if len(os.listdir(DOWNLOAD_PATH)) == 1 :
                if os.listdir(DOWNLOAD_PATH)[0]=='_finished' and len(os.listdir(READY_TO_TREAT_PATH))==0 :
                    log('NO MORE VIDEOS TO TREAT')
                    os.mkdir(f'{READY_PATH}\_finished')
                    break






    def extract_csv(self,id) :
        csvlist=[]
        with open(f'{TREATING_PATH}\{id}\{id}.csv',"r",encoding='utf-8') as f:
                            reader = csv.reader(f,delimiter=',' )
                            for row in reader :
                                csvlist.append(csvItem(id,row[0],row[1],row[2],row[3]))
        os.mkdir(f'{TREATING_PATH}\{id}\shorts')
        return csvlist
    
    def extract_tags (self,Caption):
        tags=list()
        words=Caption.split()
        for elem in words :
            if elem.startswith('#') :
                tags.append(elem.replace('#',''))
        return tags
        
    def extract_transcript(self,file,tfile) :
        model = whisper.load_model("base")
        audio = whisper.load_audio(file)
        result = model.transcribe(audio)
        text=result["segments"]
        txt=[]
        for elm in text : 
            transcript=''.join(f"[{str(elm['start'])} --> {str(elm['end'])}] {elm['text']} \n")
            txt.append(transcript)
        t=''.join(txt)
        with open(tfile ,'w' , encoding='utf-8') as f:
            f.write(t)
        log(f'Transcript file generated : {tfile}, Length : {len(t)}')

    def extract_audio(self,file) :
        video = AudioSegment.from_file(f'{READY_TO_TREAT_PATH}\{file}')
        audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        new_folder=f"{TREATING_PATH}\{file.split('====')[0]}"
        os.mkdir(new_folder)
        audio.export(f"{new_folder}\{file.split('====')[0]}.wav", format="wav")
        
        log(f"Audio file generated : {new_folder}\{file.split('====')[0]}.wav")

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
        
    def OpenAi_API(self,prompt,model="gpt-4" ) :
        openai.api_key = API_KEY
        print('OpenAI API endpoint ')
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )       
        log('API endpoint success')
        return response.choices[0].message["content"]
    
    
    def score (self,id) :
        res=[]
        splitted=[]
        with open(f'{TREATING_PATH}\{id}\{id}.txt' ,'r' , encoding='utf-8') as f:
            transcript=f.read()
        if len(transcript)>18000 :
            splitted=textwrap.wrap(transcript, 10000,replace_whitespace=False,break_long_words=False,break_on_hyphens=False,drop_whitespace=False)
        else :
            splitted.append(transcript)
        for elem in splitted :
            log(f'Getting scores from {len(elem)} character')
            try :
                res.append(self.OpenAi_API(SCORE_PROMPT(elem)))
            except :
                time.sleep(300)
                res.append(self.OpenAi_API(SCORE_PROMPT(elem)))
        x=self.extract_dict(''.join(res))
        csv_file=f'{TREATING_PATH}\{id}\{id}.csv'
        with open(csv_file,'w',encoding='utf-8',newline='') as f :
            writer = csv.writer(f)
            for elem in x :
                writer.writerow([elem['start'],elem['end'],elem['transcript'],elem['score']])
        log(f'Scores Generated for : {id} ')

    def extract_user(self,id) :
        l=[]
        with open('id.csv','r',encoding='utf-8') as f :
                        reader = csv.reader(f,delimiter=',' )
                        for row in reader :
                            l.append([row[0],row[1]])
        for elem in l : 
            if elem[0] == id :
                return str(elem[1])
            
    def extract_videos(self,list,id) :
        video=self.get_video(id)
        if video is not None :
            i=0
            n=0
            user=self.extract_user(id)
            for elem in list  :
                if float(elem.score) >= MINIMUM_SCORE and float(elem.end)-float(elem.start) <=SHORTS_MAXIMUM_LENGTH and float(elem.end)-float(elem.start) >= MINIMUM_SCORE and n< MAXIMUM_NUMBER_OF_SHORTS :
                    log(f'Cutting {float(elem.end)-float(elem.start)} seconds from {id}')
                    clip = VideoFileClip(video)
                    clip = clip.subclip(float(elem.start), float(elem.end))
                    (w, h) = clip.size
                    crop_width = h * CROP_SIZE
                    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
                    y1, y2 = 0, h
                    cropped_clip = crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
                    cropped_clip = crop(clip, width=crop_width, height=h, x_center=w/2, y_center=h/2)
                    file=f'{TREATING_PATH}\{id}\shorts\{i}.mp4'
                    cropped_clip.write_videofile(file)
                    i+=1
                    caption=self.OpenAi_API(CAPTION_PROMPT(elem.transcript))
                    tags=self.extract_tags(caption)
                    if len(tags)==0 or tags is None : 
                        tags[0]="Tiktok"
                    for elem in tags :
                        caption=caption.replace(elem,'')
                    caption=caption.replace('#','')
                    caption=caption.replace('"','')
                    caption=caption.replace('title','')
                    data = {
                    "file": f"{file}",
                    "caption": f'{caption}',
                    "tags": f"{tags}",
                    "user": f'{user}'
                                }
                    with open(f"{READY_PATH}\json_data_{uuid.uuid4()}.json", "w",encoding='utf-8') as outfile:
                        json.dump(data, outfile)
                    n=n+1
        log(f'Shorts generation completed for : {id}')



                    
    def Isvideo(self,file) :
        mime = magic.Magic(mime=True)
        filename = mime.from_file(file)
        if filename.find('video') != -1:
            return True
        else :  
            return False
    def get_video(self,id) :
        for elem in os.listdir(f'{TREATING_PATH}\{id}') :
            file=f'{TREATING_PATH}\{id}\{elem}'
            if self.Isvideo(file) :
                return file
        return None
    

                