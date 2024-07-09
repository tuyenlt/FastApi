from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

class Users(BaseModel):
    tel : str
    name : str
    address : str
    acceptance_day : str
    warranty_time : str
    
class telReq(BaseModel):
    tel : str

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database ="saunaapi"
)

cursor = db.cursor(buffered=True)

@app.get("/")
def home():
    return "this is homepage"

@app.post("/user/warranty_check")
def getWarrantyDate(req : telReq):
    try:
        cursor.execute(f"SELECT * FROM users WHERE tel = \"{req.tel}\"")
        for row in cursor.fetchall():
            user = {"name":row[1] , "acceptance_day" : row[3], "warranty_time": row[4]}
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Database error")
    
@app.post("/user/add")
def addUser(req : Users):
    try:
        query = f"INSERT INTO users(tel,name,address,acceptance_day,warranty_time) VALUES(\"{req.tel}\",\"{req.name}\",\"{req.address}\",\"{req.acceptance_day}\",\"{req.warranty_time}\")"
        cursor.execute(query)
        db.commit()
        return "add users success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Database error")
   
@app.delete("/user/delete")
def delUser(req : telReq):
    try:
        query = f"DELETE FROM users WHERE tel=\"{req.tel}\""
        cursor.execute(query)
        db.commit()
        return "delete users success"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Database error")   
    
@app.get("/user/viewall")
def viewUser():
    try:
        query = "SELECT * FROM users"
        cursor.execute(query)
        totals_user = []
        for row in cursor.fetchall():
            totals_user.append({"tel":row[0],  "name": row[1], "address" : row[2] ,"acceptance_day":row[3], "warranty_time":row[4] })
        return totals_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Database error")   
    
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)