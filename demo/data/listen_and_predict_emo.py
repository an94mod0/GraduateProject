
# after create SVM model, always listening /audio fold
# if any .wav or .mp3 add, predict its emotion and save result to txt


from __future__ import print_function
from __future__ import division
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import numpy as np
import os
import time
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import ShuffleSplit

features=[0, 1, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
emotions=["neutral","calm","happy","sad","angry","fearful","disgust","surprised"]
now=time.time()
#train model from pre-analysis features
d2_train_data=np.loadtxt("train_data.txt")
d2_label=np.loadtxt("train_label.txt")
d2_label=d2_label.astype(int)
clf=SVC(kernel="linear")
print("read train data use "+str(time.time()-now)+" s")
now=time.time()
clf.fit(d2_train_data,d2_label)
print("training use "+str(time.time()-now)+" s")
now=time.time()


#test data

def ChangeType(file_name):
    from pydub import AudioSegment
    AudioSegment.from_file(file_name,file_name.split('.')[1]).set_channels(1).set_sample_width(2).set_frame_rate(44100).export("tmp.wav",format="wav")
    return "tmp.wav"

def PredictAudio_threesecond(file_name):
    print(file_name)
    td=[]
    [Fs,x]=audioBasicIO.readAudioFile(ChangeType(file_name))
    F=audioFeatureExtraction.stFeatureExtraction(x[:Fs*3],Fs,0.05*Fs,0.025*Fs)
    #traversal whole audio (max:60mins)
    for i in range(0,300):
        F=audioFeatureExtraction.stFeatureExtraction( x[Fs*3*i:Fs*3*(i+1)],Fs,0.05*Fs,0.025*Fs )
        if F.shape[1]==119: #legal
            td.append(F[features,])
        else: #audio end
            #print("length error")
            #print(F)
            break
    test_data=np.array(td)
    print(test_data.shape)
    nsamples,nx,ny = test_data.shape
    d2_test_data = test_data.reshape((nsamples,nx*ny))
    result=clf.predict(d2_test_data)
    t=0
    print("read "+file_name+" success")
    target_path="json\\"+file_name.split("\\")[-1]
    target_path=target_path.split(".")[0]+".txt"
    pen=open(target_path,"w")
    # result is a list , emo/3s
    # look back
    for i in range(len(result)):
        line=str(int(t/60)) + ":" + str(t%60) + "~" + str(int((t+3)/60)) + ":" + str((t+3)%60) + " : " + str(emotions[result[i]-1])
        pen.write(line)
        pen.write("\n")
        t+=3
    pen.close()
    print("save json result to "+target_path)


print("start listening")
path_to_watch = "audio"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
    time.sleep (1)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added: 
        print ("Added: ", ", ".join (added))
    if removed: 
        print ("Removed: ", ", ".join (removed))
    before = after
    if len(added)>0: 
        if (added[0].split(".")[-1] == "mp3") or (added[0].split(".")[-1] == "wav"):
            print ("audio file added!")
            path=path_to_watch+"\\"+str(added[0])
            #print(path)
            PredictAudio_threesecond(path)
            print("ready to handle next audio")
            #do...