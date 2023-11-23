from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import asyncpg

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class UserLogin(BaseModel):
    username: str
    password: str


# Function to create a connection pool
async def create_connection_pool():
    return await asyncpg.create_pool(
        user='',
        password='',
        database='',
        host='localhost'
    )

@app.on_event("startup")
async def startup():
    app.state.pool = await create_connection_pool()

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close() 

# path default untuk running fungsi login()
# ngebuka file login.html yang ada di folder templates
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# path login untuk running fungsi process_login()
# process login panggil database
# nyocokin username sama password
# kalau username atau password tidak sesuai kasih error "login gagal"
@app.post("/login")
async def process_login(username: str = Form(...), password: str = Form(...)):
    print(f"Username: {username}, Password: {password}")
    user_login_instance = UserLogin(username=username, password=password)
    query = "SELECT * FROM users WHERE username = $1 AND password = $2"
    async with app.state.pool.acquire() as connection:
        result = await connection.fetchrow(query, user_login_instance.username, user_login_instance.password)
        if result:
            return {"message": "Login berhasil"}
        else:
            raise HTTPException(status_code=401, detail="login gagal")