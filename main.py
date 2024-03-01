import requests,json,random,cv2,os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp as youtube_dl


url = "https://pointercrate.com/"
auth = ("gruffelf", "password")

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'])

@app.get("/demon/sync")
def get_list():
    response = requests.get(url+"/api/v2/demons/listed/")
    with open("list.json", "w") as outfile:        
        json.dump(response.json(), outfile)    
    return {"Status": "Synced List"} 

@app.get("/demon/getdemon")
def get_demon(num: int=None):    
    with open("list.json", "r") as openfile:
        obj = json.load(openfile)        
    print(obj)
    if num != None:
        obj = [i for i in obj if i["position"] < num+1]
    level = random.choice(obj) 
    #return(obj)   
    return {"Name": level.get('name'),"Position": level.get('position'),"Video": level.get('video')[8:]}

@app.get("/demon/getcapture")
def get_demon(entry: str=""):
    url = 'https://'+entry  
    ydl_opts={}
    ydl=youtube_dl.YoutubeDL(ydl_opts)
    info_dict=ydl.extract_info(url, download=False)
    formats = info_dict.get('formats',None)     
    path=os.path.dirname(__file__) 
    for f in formats:   
        if f.get('resolution',None) == '1920x1080': 
            print('f')    
        if f.get('format_id',None) == '312':
            print('working here')
            url = f.get('url',None)
            cap = cv2.VideoCapture(url)                
            count=random.randint(300,int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-300)                
            print(count)
            cap.set(cv2.CAP_PROP_POS_FRAMES, count-1)
            ret, frame = cap.read()
            if not ret:
                break
            filename = path+'\capture.png'
            cv2.imwrite(filename.format(count), frame)        
            
            if cv2.waitKey(30)&0xFF == ord('q'):
                break
            cap.release()
            #try:
            return FileResponse(path+'\capture.png')
            #finally:
                #os.remove(path+'\capture.png')
            
