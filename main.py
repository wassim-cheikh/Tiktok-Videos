from bot.Edit_videos import edit_videos
from bot.Get_videos import get_videos
from bot.Upload_videos import upload_videos
import threading
from bot.tiktok import uploadVideo

uploadVideo('165c3c98b23a486f2008a12a7e8b14fd',r"C:\Users\Wassim Cheikh\Downloads\Download (1).mp4",'title',['aaaa'])
if __name__ == '__main__':
    def p1():
        g=get_videos()
        g.get_input()
        g.search()
        g.download_videos()
    def p2() :
                e=edit_videos()
    def p3() :
                u=upload_videos()
    P1=threading.Thread(target=p1)
    P2=threading.Thread(target=p2)
    P3=threading.Thread(target=p3)
    P1.start()
    P2.start()
    P3.start()

