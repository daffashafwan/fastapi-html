from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class UserLogin(BaseModel):
    username: str
    password: str

db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    passwd="your_password",
    database="your_database"
)

# path default untuk running fungsi login()
# ngebuka file login.html yang ada di folder templates
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# path login untuk running fungsi process_login()
# process login panggil database
# nyocokin username sama password
# kalau username atau password tidak sesuai kasih error "login gga"
@app.post("/login")
async def process_login(username: str = Form(...), password: str = Form(...)):
    print(f"Username: {username}, Password: {password}")
    user_login_instance = UserLogin(username=username, password=password)
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (user_login_instance.username, user_login_instance.password))
    result = cursor.fetchone()

    if result:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")