import requests
import json
import wave
import datetime
from os import system
from time import sleep
#変数定義
api = "https://api.p2pquake.net/v2/history?limit=1"
eqinfo = "&codes=551"
tsunamiinfo = "&codes=552"
eewinfo = "&codes=554"
eqdatan = tsunamidatan = dict
tstatus = False
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
        return "1"
    elif value == 20:
        return "2"
    elif value == 30:
        return "3"
    elif value == 40:
        return "4"
    elif value == 45:
        return "5弱"
    elif value == 50:
        return "5強"
    elif value == 55:
        return "6弱"
    elif value == 60:
        return "6強"
    elif value == 70:
        return "7"
    elif value == -1:
        return "情報なし"

def parsejson_eq(data):
    # print(type(data))
    eq = data[0]
    info = eq['earthquake']
    jouhou = eq['issue']['type']
    time = info['time']
    # print(time)
    time = datetime.datetime.strptime(time,"%Y/%m/%d %H:%M:%S")
    # print(type(time))
    # timestr = time[11:13]+"時"+time[14:16]+"分頃"
    timestr = str(time.hour) + "時" + str(time.minute) + "分頃"

    hypocenter = info['hypocenter']
    depth = hypocenter['depth']
    hyponame = hypocenter['name']
    magnitude = hypocenter['magnitude']
        
    maxshindo = info['maxScale']
    tsunami = info['domesticTsunami']
    shindo70 = shindo60 = shindo55 = shindo50 = shindo45 = shindo40 = shindo30 = shindo20 = shindo10 = ""

    kakuchi = eq['points']
    # 各地の震度情報
    for i in range(0,len(kakuchi)):
        if kakuchi[i]['scale'] == 70:
            shindo70 = shindo70 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 60:
            shindo60 = shindo60 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 55:
            shindo55 = shindo55 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 50:
            shindo50 = shindo50 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 45:
            shindo45 = shindo45 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 40:
            shindo40 = shindo40 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 30:
            shindo30 = shindo30 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 20:
            shindo20 = shindo20 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","
        elif kakuchi[i]['scale'] == 10:
            shindo10 = shindo10 + kakuchi[i]['pref'] + kakuchi[i]['addr'] + ","

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
    
    if jouhou == "ScalePrompt":
        denbun1 = jouhoustr+"を受信しました.\n"+timestr+",最大震度"+shindostr(maxshindo)+"を観測する地震がありました.\n"+tsunamistr+"\n震源は現在調査中です."
    else:
        denbun1 = jouhoustr+"を受信しました.\n"+timestr+",最大震度"+shindostr(maxshindo)+"を観測する地震がありました.\n"+tsunamistr+"\n震源は"+hyponame+",深さ"+str(depth)+"km.地震の規模を示すマグニチュードは,"+str(magnitude)+"です."
    denbun2 = "各地の震度をお伝えします.\n"
    if shindo70 != "":
        shindodenbun = "震度7を観測した地域は," + shindo70[0:len(shindo70)-1] + "です. 震度6強を観測した地域は," + shindo60[0:len(shindo60)-1] + "です. 震度6弱を観測した地域は," + shindo55[0:len(shindo55)-1] + "です. 震度5強を観測した地域は," + shindo50[0:len(shindo50)-1] + "です. 震度5弱を観測した地域は," + shindo45[0:len(shindo45)-1] + "です. 震度4を観測した地域は," + shindo40[0:len(shindo40)-1] + "です. 震度3を観測した地域は," + shindo30[0:len(shindo30)-1] + "です."
    elif shindo60 != "":
        shindodenbun = " 震度6強を観測した地域は," + shindo60[0:len(shindo60)-1] + "です. 震度6弱を観測した地域は," + shindo55[0:len(shindo55)-1] + "です. 震度5強を観測した地域は," + shindo50[0:len(shindo50)-1] + "です. 震度5弱を観測した地域は," + shindo45[0:len(shindo45)-1] + "です. 震度4を観測した地域は," + shindo40[0:len(shindo40)-1] + "です. 震度3を観測した地域は," + shindo30[0:len(shindo30)-1] + "です."
    elif shindo55 != "":
        shindodenbun = "震度6弱を観測した地域は," + shindo55[0:len(shindo55)-1] + "です. 震度5強を観測した地域は," + shindo50[0:len(shindo50)-1] + "です. 震度5弱を観測した地域は," + shindo45[0:len(shindo45)-1] + "です. 震度4を観測した地域は," + shindo40 + "です. 震度3を観測した地域は," + shindo30[0:len(shindo30)-1] + "です."
    elif shindo50 != "":
        shindodenbun = " 震度5強を観測した地域は," + shindo50[0:len(shindo50)-1] + "です. 震度5弱を観測した地域は," + shindo45[0:len(shindo45)-1] + "です. 震度4を観測した地域は," + shindo40[0:len(shindo40)-1] + "です. 震度3を観測した地域は," + shindo30[0:len(shindo30)-1] + "です."
    elif shindo45 != "":
        shindodenbun = " 震度5弱を観測した地域は," + shindo45[0:len(shindo45)-1] + "です. 震度4を観測した地域は," + shindo40[0:len(shindo40)-1] + "です. 震度3を観測した地域は," + shindo30[0:len(shindo30)-1] + "です."
    elif shindo40 != "":
        shindodenbun = "震度4を観測した地域は," + shindo40[0:len(shindo40)-1] + "です. 震度3を観測した地域は," + shindo30[0:len(shindo30)-1] + "です."
    elif shindo30 != "":
        shindodenbun = " 震度3を観測した地域は," + shindo30[0:len(shindo30)-1] + "です. 震度2を観測した地域は," + shindo20[0:len(shindo20)-1] + "です. 震度1を観測した地域は," + shindo10[0:len(shindo10)-1] + "です."
    elif shindo20 != "":
        shindodenbun = " 震度2を観測した地域は," + shindo20[0:len(shindo20)-1] + "です. 震度1を観測した地域は," + shindo10[0:len(shindo10)-1] + "です."
    elif shindo10 != "":
        shindodenbun = " 震度1を観測した地域は," + shindo10[0:len(shindo10)-1] + "です."
    # shindodenbun = ["震度7を観測した地域は," + shindo70, "震度6強を観測した地域は," + shindo65, "震度6弱を観測した地域は," + shindo60, "震度5強を観測した地域は" + shindo50, "震度5弱を観測した地域は," + shindo45, "震度4を観測した地域は," + shindo40, "震度3を観測した地域は," + shindo30]
    
    print(denbun1)
    print(shindodenbun)
    generate_wav(denbun1,8,"overview.wav")
    generate_wav(str(denbun2 + shindodenbun +"以上,地震情報をお伝えしました."),8,"shindo.wav")

    # print()
    play()

def parsejson_tsunami(data):
    global tstatus
    tmajorwarn = ""
    twarn = ""
    twatch = ""
    if data == []:
        return
    data = data[0]
    cancelled = data['cancelled']

    if cancelled:
        denbun1 = "津波予報は解除されました."
        generate_wav(denbun1,8,"toverview.wav")
        return
    elif tstatus:
        denbun1 = "津波予報が更新されました."
    else:
        denbun1 = "津波予報が発表されました."
        tstatus = True
    area = data['areas']
    for i in range(len(area)):
        if area[i]['grade'] == "MajorWarning":
            tmajorwarn = tmajorwarn + area[i]['name'] + ","
        elif area[i]['grade'] == "Warning":
            twarn = twarn + area[i]['name'] + ","
        elif area[i]['grade'] == "Watch":
            twatch = twatch + area[i]['name'] + ","
    
    denbun2 = ""

    print("大津波警報: " + tmajorwarn + "\n津波警報: " + twarn + "\n津波注意報: " + twatch)
    if tmajorwarn != "":
        denbun2 = denbun2 + "大津波警報が," + tmajorwarn[0:len(tmajorwarn)-1] + "に,発表されています."
    
    if twarn != "":
        denbun2 = denbun2 + "津波警報が," + twarn[0:len(twarn)-1] + "に,発表されています."
    
    if twatch != "":
        denbun2 = denbun2 + "津波注意報が," + twatch[0:len(twatch)-1] + "に,発表されています."
    
    denbun2 = denbun2 + "対象地域にお住まいのかたは,直ちに海岸から離れてください."
    generate_wav(denbun1,8,"toverview.wav")
    generate_wav(denbun2,8,"tsunami.wav")

# 更新チェック
def datacheck():
    global eqdatao, eqdatan, tsunamidatao, tsunamidatan, equpdate, tsunamiupdate
    # データ入れ替え
    eqdatao = eqdatan
    eqdatan = get_latest_data(eqinfo)
    tsunamidatao = tsunamidatan
    tsunamidatan = get_latest_data(tsunamiinfo)

    # 新旧比較
    # 0=更新なし 1=更新あり
    if eqdatao == eqdatan:
        equpdate = 0
    else:
        equpdate = 1
    
    if tsunamidatao == tsunamidatan:
        tsunamiupdate = 0
    else:
        tsunamiupdate = 1
    

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

def play():
    system("afplay ./overview.wav")
    system("afplay ./shindo.wav")

# mainloop
while 1:
    datacheck()
    print("Status: EQ=" + str(equpdate) + " TSUNAMI=" + str(tsunamiupdate))
    if equpdate==1:
        parsejson_eq(eqdatan)
    if tsunamiupdate==1:
        parsejson_tsunami(tsunamidatan)
    sleep(4)

