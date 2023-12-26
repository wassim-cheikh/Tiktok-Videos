class userItem() :
    def __init__(self,username,session_id) -> None:
        self.username=username
        self.session_id=session_id
    def __str__(self) -> str:
        return f'[ Username : {self.username} , Session Id : {self.session_id}]'


class KeywordItem() :
    def __init__(self , Keyword , num_of_videos,max_length,min_length,user:userItem) -> None:
        self.Keyword=Keyword
        self.user=user
        self.num_of_videos=num_of_videos
        self.max_length=max_length
        self.min_length=min_length
    def __str__(self) -> str:
        return f'[ Keyword : {self.Keyword} ,  num_of_videos : {self.num_of_videos} ,max_length: {self.max_length} min_length : {self.min_length} , user : {self.user}]' 
    
class videoItem() :
    def __init__(self,id,title,link,length,Keyword:KeywordItem) -> None:
        self.Keyword=Keyword
        self.id=id
        self.title=title
        self.link=link
        self.length=length
    def __str__(self) -> str:
        return f'[ id : {self.id} ,title : {self.title} , link : {self.link} , length : {self.length} Keyword : {self.Keyword} ]' 
    
class csvItem():
    def __init__(self,id,start,end,transcript,score) -> None:
        self.id=id
        self.start=start
        self.end=end
        self.transcript=transcript
        self.score=score
    def __str__(self) -> str:
        return f'[ id : {self.id} , start : {self.start} , end : {self.end} , transcript : {self.transcript} , score : {self.score} ]'