from fastapi import FastAPI, Request
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
    name="static"
)

relations = {}

roomsInfo = {}

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = 'index.html'
    )

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

@app.get('/check_room/{room_id}')
async def check_room(room_id: str):
    if room_id in roomsInfo:
        return JSONResponse(content={'link': f'/rooms/{room_id}', 'error': 0})
    else:
        return JSONResponse(content={'link': f'', 'error': 1})

@sio.event
async def disconnect(sid):
    if sid not in relations:
        return

    room = relations[sid]['room']

    if room in roomsInfo:
        roomsInfo[room]['users'].remove(sid)

        if not roomsInfo[room]['users']:
            del roomsInfo[room]

    del relations[sid]

@sio.on('join_room')
async def join_room(sid, data):
    relations[sid] = {
        'name': data['username'],
        'room': data['room_id']
    }
    await sio.enter_room(sid, data['room_id'])

    if relations[sid]['room'] not in roomsInfo:
        roomsInfo[data['room_id']] = {
            'users': [sid],
            'current_video': '',
            'current_time': 0,
            'playing': False,
            'host_sid': sid
        }
    else:
        roomsInfo[relations[sid]['room']]['users'].append(sid)
    await sio.emit('join_room', {
        'curT': roomsInfo[relations[sid]['room']]['current_time'],
        'curVid': roomsInfo[relations[sid]['room']]['current_video'],
        'isPlaying': roomsInfo[relations[sid]['room']]['playing']
        }, to=sid)

@sio.on('load_video')
async def load_video(sid, data):
    roomsInfo[relations[sid]['room']]['current_video'] = data['url']
    roomsInfo[relations[sid]['room']]['current_time'] = 0
    roomsInfo[relations[sid]['room']]['playing'] = False
    await sio.emit('load_video', data, room=relations[sid]['room'])

@sio.on('set_current_time')
async def set_current_time(sid, data):
    if sid not in relations:
        return
    if roomsInfo[relations[sid]['room']]['host_sid'] != sid:
        return
    
    room = relations[sid]['room']

    if room not in roomsInfo:
        return

    roomsInfo[room]['current_time'] = data['currentT']

@sio.on('play_video')
async def play_video(sid, data):
    roomsInfo[relations[sid]['room']]['playing'] = True
    await sio.emit('play_video', data, room=relations[sid]['room'], skip_sid=sid)

@sio.on('pause_video')
async def pause_video(sid):
    roomsInfo[relations[sid]['room']]['playing'] = False
    await sio.emit('pause_video', room=relations[sid]['room'], skip_sid=sid)