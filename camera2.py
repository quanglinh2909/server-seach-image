import cv2
import face_recognition
import os
import numpy as np
import service
import base64
import uuid
import requests
from io import BytesIO
from PIL import Image

cap = cv2.VideoCapture(1)

def get_endcode(data):
    arrIdAddict=[]
    arrEncode =[]
    for row in data:
        arrEncode.append(row['data'])
        arrIdAddict.append(row['idAddict'])
    return {"encode":arrEncode,"id":arrIdAddict}
def frame_to_base64(frame):
    return base64.b64encode(frame)
arrImage=[]

def find_by_array(array,value):
    for item in array:
        if item == value:
            return True
    return False
while True:
    # ret nếu đọc đúng trả về true false frame trả về khung hình camera
    ret, frame = cap.read()
    framS = cv2.resize(frame, (0, 0), None, fx=0.5, fy=0.5)
    FRAMsAVE = framS
    framS = cv2.cvtColor(framS, cv2.COLOR_BGR2RGB)

    # xác định vị trí khuôn mặt trên cam và encode hình ảnh trên cam
    facecurFrame = face_recognition.face_locations(framS)  # lấy từng khuôn mặt và vị trí khuôn mặt hiện tại
    encodecurFrame = face_recognition.face_encodings(framS)

    for encodeFace, faceLoc in zip(encodecurFrame, facecurFrame):  # lấy từng khuôn mặt và vị trí khuôn mặt hiện tại theo cặp
        encodeListKnow = get_endcode(service.getData())
        matches = face_recognition.compare_faces(encodeListKnow['encode'], encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow['encode'], encodeFace)
        matchIndex = np.argmin(faceDis)  # đẩy về index của faceDis nhỏ nhất
        # print(faceDis)
        if faceDis[matchIndex] < 0.50:
            pil_img = Image.fromarray(frame)
            buff = BytesIO()
            pil_img.save(buff, format="png")
            new_image_string = base64.b64encode(buff.getvalue())
            name = encodeListKnow['id'][matchIndex]
            # cv2.imwrite("save/" + name + ".jpg", FRAMsAVE)
            # cv2.imwrite("C:/Users/RD98/Documents/GitHub/test/chane-file/demo/" + name + ".jpg", FRAMsAVE)
            # arrImage.append()
            # print(type(FRAMsAVE))
            if (find_by_array(arrImage,name)) == False:
                arrImage.append(name)
                response = requests.post("http://192.168.100.74:3100/api/find-addict-by-image/receive-file",
                                     data={'data': new_image_string,'id':name})
            # print(arrImage)
        else:
            name = "Unknow"

        # print tên lên frame
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('show cam', frame)
    if cv2.waitKey(1) == ord("q"):  # độ trễ 1/1000s , nếu bấm q sẽ thoát
        break
cap.release()  # giải phóng camera
cv2.destroyAllWindows()  # thoát tất cả các cửa sổ

