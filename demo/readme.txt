- 建構情緒預測模型並開始監聽
- 建立關鍵字偵測架構並開始監聽
- 建立網頁DOM結構並開始監聽
while 新增一筆音訊:
    1- listen_and_predict_emo.py(under anaconda python2)分析音訊, 將結果(情緒)儲存result.txt
    2- listen_and_count_keyword.py分析音訊, 將結果(關鍵字)儲存為keyword.json及keyword_time.json
    3- listen_and_gen_json.py(under python3)讀取result.txt與keyword.json, 將整併結果儲存eventdrop.json
    4- 偵測到eventdrop.json(時間軸)或keyword.json(文字雲)後刷新頁面呈現最新結果