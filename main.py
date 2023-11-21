from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def process_login(username: str = Form(...), password: str = Form(...)):
    # Here, you can implement your authentication logic
    # For demonstration purposes, let's print the received credentials
    print(f"Username: {username}, Password: {password}")
    return {"message": "Login successful"}