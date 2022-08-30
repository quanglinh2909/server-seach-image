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
        start_time = time.time()
        data =  service.search(item.url)
        end_time = time.time()
        print("thơi gian 1: ", end_time - start_time)
        return data

    except:
        return("sai duong dan")
@app.post("/insert")
async def insert_image(item:IsertItem):
    print(item.id,item.url)
    try:
        isE = service.isExist(item.id)
        print(3)
        if len(isE) == 0:
            print("1")
            start_time = time.time()
            data =  service.insert(item.id,item.url)
            end_time = time.time()
            print("thơi gian 1: ", end_time - start_time)
            return data
        else:
           print(2)
           return service.update(item.id, item.url)

    except:
        return("sai duong dan")
@app.put("/update")
async def update_image(item:IsertItem):
    try:
        start_time = time.time()
        data =  service.update(item.id,item.url)
        end_time = time.time()
        print("thơi gian 1: ", end_time - start_time)
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


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info",host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()