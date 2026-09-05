let player;
const videoBtn = document.getElementById('newVideoBtn');
const urlTextInput = document.getElementById('videoUrl');
const socket = io();
let isRemote = false;
let playerReady = false;
let pendingRoomState;
let roomJoined = false;

videoBtn.addEventListener('click', () => {
    const uurl = urlTextInput.value;
    socket.emit('load_video', {url: uurl})
})

function onYouTubeIframeAPIReady() {

    player = new YT.Player('player', {
        height: '390',
        width: '640',

        videoId: '',

        playerVars: {
            autoplay: 0,
            playsinline: 1,
            rel: 0,
            controls: 1,
            origin: window.location.origin
        },

        events: {
            onReady: onPlayerReady,
            onStateChange: onPlayerStateChange,
            onError: onPlayerError
        }
    });
}

setInterval(() => {
    if (!player || !playerReady || !roomJoined) return;
    socket.emit('set_current_time', {currentT: player.getCurrentTime()})
}, 200)

function onPlayerReady(event) {
    event.target.mute();
    playerReady = true;
    console.log("Плеер готов!");
    socket.emit('join_room', {
        room_id: ROOM_ID,
        username: localStorage.getItem('username')
    })
}

function onPlayerStateChange(event) {
    console.log(event.data)
    if (event.data == YT.PlayerState.PLAYING) {
        if (!isRemote) {
            socket.emit('play_video', {
                currentTime: player.getCurrentTime()
            });
        } else {
            isRemote = false;
        }
    } else if (event.data == YT.PlayerState.PAUSED) {
        if (!isRemote) {
            socket.emit('pause_video');
        } else {
            isRemote = false;
        }
    } else if (event.data == YT.PlayerState.CUED) {
        if (!pendingRoomState) {
        return;
        }
        const state = pendingRoomState;
        pendingRoomState = null;

        if (state.isPlaying) {
            player.playVideo();
        }
    }
}

function onPlayerError(event) {
    console.log("YouTube error code:", event.data);
}

function loadVideo(url, startSec=0) {
    const parsedUrl = new URL(url);
    const finalId =  parsedUrl.searchParams.get('v');
    player.cueVideoById(finalId, startSec);
}

socket.on('load_video', (data) => {
    loadVideo(data.url)
})

socket.on('play_video', (data) => {
    isRemote = true;
    player.seekTo(data.currentTime, true);
    player.playVideo();
})

socket.on('pause_video', () => {
    isRemote = true;
    player.pauseVideo();
})

socket.on('join_room', (data) => {
    roomJoined = true;
    
    if (!data.curVid) {
        return
    }
    pendingRoomState = data;
    loadVideo(data.curVid, data.curT);
})