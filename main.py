from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import service
import time

class MyItem(BaseModel):
    url:str
class IsertItem(BaseModel):
    url:str
    id:str

app = FastAPI()

@app.get("/")
async def home():
    return "day la hom"
@app.post("/search")
async def search_image(item:MyItem):
    try:
        data =  service.search(item.url)
        return data

    except:
        return("sai duong dan")
@app.post("/insert")
async def insert_image(item:IsertItem):
    try:
        isE = service.isExist(item.id)
        if len(isE) == 0:
            data =  service.insert(item.id,item.url)
            return data
        else:
           return service.update(item.id, item.url)

    except:
        return("sai duong dan")
@app.put("/update")
async def update_image(item:IsertItem):
    try:
        data =  service.update(item.id,item.url)
        return data
    except:
        return("sai duong dan")

@app.delete("/delete/{id}")
def delete(id: str):
    try:
        return service.delete(id)
    except:
        return ("sai duong dan")

@app.on_event("startup")
async def startup_event():
    print("khoi dong server")
    try:
        service.init_server("http://192.168.100.74:3100/api/addict/get-all")
    except:
        print("loi server")


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info",host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()