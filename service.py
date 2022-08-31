import sqlite3

import sqlite3
import cv2
import face_recognition
import urllib.request
import numpy
import requests
CLIENT_HOST = 'http://192.168.100.74:3100/'
def getData():
    conn = sqlite3.connect('data/data.db')
    cursor = conn.execute("SELECT * FROM encode")
    rows = cursor.fetchall()
    conn.close()
    results=[]
    for r in rows:
        item={
            "id":r[0],
            "idAddict":r[1],
            "data":numpy.fromstring(r[2], dtype=float, sep=','),
            "url":r[3]
        }
        results.append(item)
    return results
def encode(url):
    response = urllib.request.urlopen(url)
    imgCheck = face_recognition.load_image_file(response)
    imgCheck = cv2.cvtColor(imgCheck, cv2.COLOR_BGR2RGB)
    encodeCheck = face_recognition.face_encodings(imgCheck)[0]
    return ','.join(str(x) for x in encodeCheck.tolist())
def insert(id,url):
    conn = sqlite3.connect('data/data.db')
    sql =  """
    INSERT INTO encode(idAddict,data,url) values (?,?,?)
     """
    cur = conn.cursor()
    data = conn.execute(sql,(id,encode(url),url))
    conn.commit()
    conn.close()
    return  cur.lastrowid

def update(id,url):
    conn = sqlite3.connect('data/data.db')
    sql =  """Update encode set data = ?, url = ? where idAddict = ?"""
    cur = conn.cursor()
    data = conn.execute(sql, (encode(url),url,id))
    conn.commit()
    conn.close()
    return cur.lastrowid
# update("1","http://192.168.100.74:3100/2022823/2022-08-23T04-00-19.156Z-2022-08-01t02-44-53.823z-anh-gai-xinh-cuc-dep.jpg")
def isExist(id):
    conn = sqlite3.connect('data/data.db')
    cursor = conn.execute("SELECT * FROM encode where  idAddict = ?",(id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
def delete(id):
    conn = sqlite3.connect('data/data.db')
    sql = """DELETE from encode where idAddict = ?"""
    cur = conn.cursor()
    data = conn.execute(sql, (id,))
    conn.commit()
    conn.close()
    return cur.lastrowid
def search(url):
    response = urllib.request.urlopen(url)
    imgCheck = face_recognition.load_image_file(response)
    imgCheck = cv2.cvtColor(imgCheck, cv2.COLOR_BGR2RGB)
    encodeCheck = face_recognition.face_encodings(imgCheck)[0]
    my_list = []
    for row in getData():
        results = face_recognition.compare_faces([row['data']], encodeCheck)
        if results[0] == True:
            faceDis = face_recognition.face_distance([row['data']], encodeCheck)
            my_list.append({'data': faceDis[0],  'id': row['idAddict']})
    return my_list
# print(insert("1","http://192.168.100.74:3100/default/16.jpg"))
# data =  numpy.array(getData()[0][2])
# print(search("http://192.168.100.74:3100/2022823/2022-08-23T04-00-19.156Z-2022-08-01t02-44-53.823z-anh-gai-xinh-cuc-dep.jpg"))

# for i in range(1,1000):
#     insert(i,"http://192.168.100.74:3100/2022823/2022-08-23T04-00-19.156Z-2022-08-01t02-44-53.823z-anh-gai-xinh-cuc-dep.jpg")

def check_data_not_none(id:str,url:str):
    dataData = getData()
    check = False
    for item in dataData:
       if item['idAddict'] == id:
           if item['url'].endswith(url) == False:
               urlImage = ''.join([CLIENT_HOST,url])
               try:
                    update(id,urlImage)
               except:
                    return False
           check = True
    # print(id,url)
    if check == False:
        urlImage = ''.join([CLIENT_HOST, url])
        try:
            insert(id, urlImage)
            return True
        except:
            return False


def check_data_none(id:str,url:str):
    dataData = getData()
    for item in dataData:
        if item['idAddict'] == id:
            delete(id)
def check_remove(response):
    dataData = getData()
    for item2 in dataData:
        check = False
        for item in response:
            if item['ID'] == item2['idAddict']:
                check = True
                break
        if check == False:
           delete(item2['idAddict'])
def init_server(url:str):
    response = requests.get(url).json()
    check_remove(response)
    for item in response:
        if item['ImgLink'] != None:
            check_data_not_none(item['ID'],item['ImgLink'])
        else:
            check_data_none(item['ID'], item['ImgLink'])

# init_server("http://192.168.100.74:3100/api/addict/get-all")