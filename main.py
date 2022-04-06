import requests
import json
import wave
from time import sleep
#変数定義
api = "https://api.p2pquake.net/v2/history?limit=1"
eqinfo = "&codes=551"
tsunamiinfo = "&codes=552"
eewinfo = "&codes=554"
eqdatan = tsunamidatan = dict
# eqinfo = 551
# tsunamiinfo = 552

#APIから最新データ取得 JSONで返却
def get_latest_data(data):
    raw = requests.get(api+data)
    # print(type(raw))
    text=raw.text
    return json.loads(text)

# def latest_json(data):
#     return json.load(get_latest_data(data))

def shindostr(value):
    if value == -1:
        return None
    elif value == 10:
        return "震度1"
    elif value == 20:
        return "震度2"
    elif value == 30:
        return "震度3"
    elif value == 40:
        return "震度4"
    elif value == 45:
        return "震度5弱"
    elif value == 50:
        return "震度5強"
    elif value == 60:
        return "震度6弱"
    elif value == 65:
        return "震度6強"
    elif value == 70:
        return "震度7"
    elif value == -1:
        return "震度の情報はありません"

def parsejson_eq(data):
    # print(type(data))
    eq = data[0]
    info = eq['earthquake']
    jouhou = eq['issue']['type']
    time = info['time']
    timestr = time[11:13]+"時"+time[14:16]+"分頃"

    hypocenter = info['hypocenter']
    depth = hypocenter['depth']
    hyponame = hypocenter['name']
    magnitude = hypocenter['magnitude']
        
    maxshindo = info['maxScale']
    tsunami = info['domesticTsunami']
    shindo70 = shiindo65 = shindo60 = shindo50 = shindo45 = shindo40 = shindo30 = shindo20 = shindo10 = ""

    kakuchi = eq['points']
    # 各地の震度情報
    for i in range(0,len(kakuchi)):
        if kakuchi[i]['scale'] == "70":
            shindo70 = shindo70 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "65":
            shindo65 = shindo65 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "60":
            shindo60 = shindo60 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "50":
            shindo50 = shindo50 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "45":
            shindo45 = shindo45 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "40":
            shindo40 = shindo40 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "30":
            shindo30 = shindo30 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "20":
            shindo20 = shindo20 + kakuchi[i]['pref'] + kakuchi[i]['addr']
        elif kakuchi[i]['scale'] == "10":
            shindo10 = shindo10 + kakuchi[i]['pref'] + kakuchi[i]['addr']

    #print(eq['points'])
    # 電文作成
    if jouhou == "ScalePrompt":
        jouhoustr = "震度速報"
    elif jouhou == "Destination":
        jouhoustr = "震源に関する情報"
        return
    elif jouhou == "ScaleAndDestination":
        jouhoustr = "震源･震度に関する情報"
    elif jouhou == "DetailScale":
        jouhoustr = "各地の震度に関する情報"
    elif jouhou == "Foreign":
        jouhoustr = "遠地地震に関する情報"
    elif jouhou == "Other":
        jouhoustr = "その他の情報"
        return


    if tsunami == "None":
        tsunamistr = "この地震による津波の心配はありません."
    elif tsunami == "Unknown":
        tsumanistr = "津波の有無は現在不明です."
    elif tsunami == "Checking":
        tsunamistr = "津波の有無は現在調査中です."
    elif tsunami == "NonEffective":
        tsunamistr = "この地震によって,若干の海面変動が予想されますが,被害の心配はありません."
    elif tsunami == "Watch":
        tsunamistr = "津波注意報が発表されています.今後の情報に警戒してください."
    elif tsunami == "Warning":
        tsunamistr = "津波予報が発表されています.今後の情報に警戒してください."
    denbun1 = jouhoustr+"を受信しました.\n"+timestr+",最大"+shindostr(maxshindo)+"を観測する地震がありました.\n"+tsunamistr+"\n震源は"+hyponame+",深さ"+str(depth)+"km.地震の規模を示すマグニチュードは,"+str(magnitude)+"です."
    denbun2 = "各地の震度をお伝えします.\n"
    
    print(denbun1)
    generate_wav(denbun1)

    print()

def parsejson_tsunami(data):
    None

# 更新チェック
def datacheck():
    global eqdatao, eqdatan, tsunamidatao, tsunamidatan, equpdate, tsunamiupdate
    # データ入れ替え
    eqdatao = eqdatan
    eqdatan = get_latest_data(eqinfo)
    tsunamidatao = tsunamidatan
    tsunamidatan = None#get_latest_data(tsunamiinfo)

    # 新旧比較
    # 0=更新なし 1=更新あり
    if eqdatao == eqdatan:
        equpdate = 0
    else:
        equpdate = 1
    
    if tsunamidatao == tsunamidatan:
        tsunamiupdate = 0
    else:
        tsunamiupdate = 0
    

def gentalk(text):
    None

def generate_wav(text, speaker=8, filepath='./audio.wav'):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()

# mainloop
while 1:
    datacheck()
    if equpdate==1:
        parsejson_eq(eqdatan)
    if tsunamiupdate==1:
        parsejson_tsunami(tsunamidatan)
    sleep(4)

