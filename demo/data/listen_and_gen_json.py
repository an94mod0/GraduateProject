#read txt, output JSON
import os
import time
import json
import io

def generateJSON(txtpath,jsonpath):
    with io.open(jsonpath,"r", encoding='utf8') as f:
        obj=json.load(f,encoding='utf-8')
        wordList=[]
        #print(obj)
        #print(list(obj.keys()))
        for k in list(obj.keys()):
            for t in obj[k]:
                wordList.append( (t,k) )
        wordList.sort()
    full_data=[{"name":"happy","data":[]},{"name":"fearful","data":[]},{"name":"calm","data":[]},{"name":"angry","data":[]},{"name":"sad","data":[]},{"name":"disgust","data":[]},{"name":"surprised","data":[]},{"name":"neutral","data":[]}]
    with open(txtpath,"r") as f:
        for line in f:
            date="2019/01/11 00:"+line.split('~')[0]
            second=int(line.split('~')[0].split(":")[0])*60+int(line.split('~')[0].split(":")[1])
            keyword=""
            if len(wordList)>0:
                #print(wordList[0][0])
                while wordList[0][0]<second+3:
                    if keyword=="":
                        keyword=wordList[0][1]
                    else:
                        keyword=keyword+", "+wordList[0][1]
                    wordList.pop(0)
                    if len(wordList) is 0:
                        break
                #print(keyword)
            emo_time={ "message":keyword , "date":date }
            for obj in full_data:
                if obj['name']==line.split(':')[3][1:-1]:
                    obj['data'].append(emo_time)
    file_name_json=txtpath+"eventdrop.json"
    file_name_json=txtpath.split("\\")[1].split(".")[0]+"_eventdrops.json"
    file_name_json="eventdrops.json"
    pen=open(file_name_json,"w",encoding='utf8')
    pen.write(str(full_data).replace("'",'"')) # JSON format
    print("save eventdrops data at "+file_name_json)
    pen.close()

#generateJSON("json\\v8-left.txt","json\\v8-left.wav_wordtime.json")
print("start listening")
path_to_watch = "json" # path of audio's location
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
waitJSON=False
txtpath=""
jsonpath=""
while 1:
    time.sleep (1)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    before = after
    if len(added)>0: 
        print(added[0])
        if not waitJSON and added[0].split(".")[-1] == "txt":
            print("find "+added[0]+", waiting next file...")
            waitJSON=True
            txtpath=path_to_watch+"\\"+str(added[0])
        if waitJSON and added[0].split(".")[-1] == "json":
            print("all ready, generating json file...")
            waitJSON=False
            jsonpath=path_to_watch+"\\"+str(added[0])
            generateJSON(txtpath,jsonpath)