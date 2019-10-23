import os
import time
import wave
import contextlib
import math
import speech_recognition
#from os import listdir
#from os.path import isfile, isdir, join
from pydub import AudioSegment
import jieba
import re
import json
import sys
# 清理文章字詞
def clean_irr_words(ob_string):
    """         去除英文及數字         """
    RE = re.search(r'[0-9a-zA-Z]+', ob_string)
    while RE:
        ob_string = ob_string.replace(RE.group(), '')
        RE = re.search(r'[0-9a-zA-Z]+', ob_string)
    """         去除底線            """
    RE = re.search(r'_+', ob_string)
    while RE:
        ob_string = ob_string.replace(RE.group(), '')
        RE = re.search(r'_+', ob_string)
    return ob_string

# 斷詞停用詞設定
def setting_stopwords(Set):
    with open('jieba_dict/mystopwords.txt', 'r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            Set.add(stopword.strip('\n'))

# 醫療字詞設定
def setting_medwords(Set):
    with open('jieba_dict/mymedword.txt', 'r', encoding = 'utf-8') as medwords:
        for medword in medwords:
            RE = re.search(r'\s[0-9]+\s[a-z]\n[\s]*', medword)
            while RE:
                medword = medword.replace(RE.group(), '')
                RE = re.search(r'\s[0-9]+\s[a-z]\n[\s]*', medword)
            # print(medword)
            Set.add(medword)

# 斷詞吐list
def tokenize(the_string):
    if result:
        result.clear()
    the_string = clean_irr_words(the_string)
    words = jieba.cut(the_string)
    for word in words:
        if word not in stopword_set:
            result.append(word)
    return result

def WordCloud(file_path,file_name):
    result_dic = dict()
    #得到醫療關鍵字群 keywors_list
    file = open('doctor_keywords.txt','r')
    keywords_list = file.readlines()
    for x in range(len(keywords_list)):
        keywords_list[x] = keywords_list[x][:-1]
    
    #start analyzing audio
    sound = AudioSegment.from_file(file_path)
    times = math.ceil(sound.duration_seconds)#向上取整數
    r = speech_recognition.Recognizer()
    n = 0 # for offset
    m = 3 #for duration
    #start google API
    cnt=0
    nowtime=time.time()
    totaltime=0
    print("檢索關鍵字中...預計花費: "+str(int(times)*2)+" 秒")
    for x in range(int(times)*2):

        cnt+=1
        persent=cnt/int(times)*50
        
        progress=str(float('%.2f'% (persent)))+"%"
        #sys.stdout.write(progress)
        print(".",end="")
        sys.stdout.flush()
        #print("第",n,"秒")
        with speech_recognition.AudioFile(file_path) as source:
            audio = r.record(source, offset = n, duration = m)
            n = n + 0.5
        try:
            words = r.recognize_google(audio,language='zh-tw')
            #print(words,)
            #count the keywords
            for y in tokenize(words):
                if y not in result_dic.keys(): #不在字典內則新增
                    if y in keywords_list: #在醫療關鍵字群內要著色+儲存出現時間
                        result_dic.update({y:{"times":1,"draw":True}})
                    else:
                        result_dic.update({y:{"times":1,"draw":False}})
                else:
                    result_dic[y]["times"] += 1
                if y not in timeword_dic.keys(): #不在字典內則新增
                    if y in keywords_list: #在醫療關鍵字群內要儲存出現時間
                        timeword_dic.update({y:[n]})
                else:
                    timeword_dic[y].append(n)            #print(words,",end")
            #print(result_dic)
        except:
            #print("voice error")
            pass
        spendtime=time.time()-nowtime
        totaltime+=spendtime
        nowtime=time.time()
        #print("use "+str(spendtime))
        #print("average time :"+str(totaltime/cnt) ) # use 1 second in average
    #output json file
    target_path="json\\"+file_path.split("\\")[1].split(".")[0]+"_keyword.json";
    target_path="wordcloud.json"
    with open(target_path, "w",encoding='utf-8') as f:
        json.dump(result_dic,f,ensure_ascii=False,sort_keys=True, indent=4)
    print("save keyword counts at "+target_path)
    clean_timeword(file_name)


def clean_timeword(target_path):  
    for j in timeword_dic.keys():
        #print("origin",timeword_dic[j])
        for q in range(len(timeword_dic[j])):
            k = timeword_dic[j][q] #先把第一個遇到的數字抓出來
            if k != -1:
                for z in range(len(timeword_dic[j])-q-1): #把 k+3跟後面的數字比較，如果 k+3>後面的數字，就把這個數字廢掉
                    if k + 3 > timeword_dic[j][q+z+1]:
                        timeword_dic[j][q+z+1] = -1
                    else:
                        break
        #print("has -1 :",timeword_dic[j])
        while (-1 in timeword_dic[j]):
            timeword_dic[j].remove(-1)
        #print("clean",timeword_dic[j])
    #output json file
    target_path="json\\"+target_path.split("_")[0]+"_wordtime.json";
    with open(target_path, "w",encoding='utf-8') as f:
        json.dump(timeword_dic,f,ensure_ascii=False,sort_keys=True, indent=4)
    timeword_dic.clear()
    print("save time and word at "+target_path)


#declare variables
result = []
timeword_dic = dict()
stopword_set = set()
medword_set = set()
jieba.set_dictionary('jieba_dict/dict.txt.big')
jieba.load_userdict('jieba_dict/mymedword.txt')
setting_stopwords(stopword_set)  # 斷詞停用詞設定
setting_medwords(medword_set)

file = open('doctor_keywords.txt','r')
keywords_list = file.readlines()

for x in range(len(keywords_list)):
    keywords_list[x] = keywords_list[x][:-1]

#listen part
print("start listening")
path_to_watch = "audio" # path of audio's location
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
    time.sleep (1)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    before = after
    if len(added)>0: 
        if (added[0].split(".")[-1] == "mp3") or (added[0].split(".")[-1] == "wav"):
            print ("audio file added!")
            path=path_to_watch+"\\"+str(added[0])
            print(path)
            WordCloud(path,str(added[0]))
            print("done")