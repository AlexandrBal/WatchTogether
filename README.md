# WatchTogether

WatchTogether is a real-time application for watching videos together.

Create a room, share its code with your friends, and watch videos together. Users in the same room receive player state updates and can communicate through a shared chat.

The project is being developed as a full web application with real-time interaction between clients.

## Features

- room creation;
- joining a room using a room code;
- participant list;
- room host identification;
- video loading;
- playback synchronization;
- video position synchronization;
- shared chat;
- message history for new participants;
- input validation;
- real-time communication using Socket.IO.

## Tech Stack

### Backend

- Python
- FastAPI
- Python-SocketIO
- Pydantic
- Uvicorn

### Frontend

- HTML
- CSS
- JavaScript
- Socket.IO Client
- YouTube IFrame API

## Installation

### Requirements

- Python 3.11+
- Git

### Clone the repository

```bash
git clone https://github.com/AlexandrBal/WatchTogether.git
cd WatchTogether
```

### Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Running

Start the application with:

```bash
uvicorn backend.main:socket_app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Open the address in your browser to use the application.

## Production

To run the application without the development auto-reloader:

```bash
uvicorn backend.main:socket_app --host 0.0.0.0 --port 8000
```

## Development

During development, use:

```bash
uvicorn backend.main:socket_app --reload
```

The `--reload` option automatically restarts the server when Python files are changed.

## How It Works

Each room has its own state and connected users.

```text
┌─────────────────┐
│     Browser     │
│      User 1     │
└────────┬────────┘
         │
         │ Socket.IO
         ▼
┌─────────────────┐
│     FastAPI     │
│   + Socket.IO   │
│                 │
│   Room State    │
│   Messages      │
└────────┬────────┘
         │
         │ Socket.IO
         ▼
┌─────────────────┐
│     Browser     │
│      User 2     │
└─────────────────┘
```

When a user changes the player state, the client sends an event to the server. The server processes the event and broadcasts the updated state to other users in the same room.

The same approach is used for:

- play/pause;
- changing the current video position;
- loading a new video;
- sending messages;
- joining a room;
- leaving a room.

## Room State

A room stores the information required to synchronize its users:

```text
Room
├── room_id
├── users
├── current_video
├── current_time
└── playing
```

The current state can be sent to a user when they join an existing room, allowing them to synchronize with the current session.

## Real-time Communication

Socket.IO is used for communication between connected clients and the server.

A simplified flow looks like this:

```text
Client
   │
   │ player_state
   ▼
Server
   │
   ├──────────────► Client
   │
   └──────────────► Client
```

This allows multiple clients to receive updates without constantly polling the server with HTTP requests.

## YouTube Integration

The YouTube IFrame API is used to control the video player in the browser.

Player events are handled by JavaScript and synchronized between users through Socket.IO.

```text
YouTube Player
      │
      ▼
  JavaScript
      │
      ▼
  Socket.IO
      │
      ▼
   FastAPI
      │
      ▼
 Other clients
```

## Roadmap

- [ ] Add more automated tests
- [ ] Improve player synchronization
- [ ] Handle user reconnection
- [ ] Improve room interface
- [ ] Add support for additional video platforms
- [ ] Move room state from process memory to persistent storage
- [ ] Add database support
- [ ] Add Docker configuration
- [ ] Prepare production deployment
