import sqlite3

import sqlite3
import cv2
import face_recognition
import csv
import json
import urllib.request
import numpy
import time

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
            "data":numpy.fromstring(r[2], dtype=float, sep=',')
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
    print(id)
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
#
def demo(id,url):
        isExi = isExist("2")
        if len(isExi) == 0:
            print("1")
            # start_time = time.time()
            data =  insert(id,url)
            # end_time = time.time()
            # print("thơi gian 1: ", end_time - start_time)
            # return data
        else:
           print(2)
           # return service.update(item.id, item.url)




# demo("A9B20AEA-3628-ED11-9687-A266FAE0D072","http://192.168.100.74:3100/2022830/2022-08-30t07-59-43.121z-aaron_peirsol_0002.jpg")