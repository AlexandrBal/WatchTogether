from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
import secrets
import socketio

app = FastAPI()

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
    )

socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

templates = Jinja2Templates(directory='templates')
templates.env.cache = None

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static")

relations = {}

@app.get('/')
async def index():
    return FileResponse("static/index.html")

@app.post('/create_room')
async def create_room():
    room_id = secrets.token_urlsafe(16)

    link = f'/rooms/{room_id}'

    return JSONResponse(content={
        'room_id': room_id,
        'link': link
    })

@app.get('/rooms/{room_id}')
async def get_room(room_id: str, request: Request):
    return templates.TemplateResponse(request=request, name='room.html', context={
        'room_id': room_id
    })

@sio.on('join_room')
async def join_room(sid, data):
    relations[sid] = {
        'name': data['username'],
        'room': data['room_id']
    }
    await sio.enter_room(sid, data['room_id'])

@sio.on('load_video')
async def load_video(sid, data):
    await sio.emit('load_video', data, room=relations[sid]['room'])