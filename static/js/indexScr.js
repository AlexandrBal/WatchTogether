const roomBtn = document.getElementById("createRoomBtn");
const newRoomCode = document.getElementById("parag");
const roomId = document.getElementById('roomID');
const roomInfo = document.getElementById("roomInfo");

roomBtn.addEventListener('click', async () => {
    const response = await fetch("/create_room", {method: "POST"});
    const data = await response.json();

    newRoomCode.innerHTML = `Комната создана: <a href='${data.link}'>Перейти</a>`;
    roomId.innerText = data.room_id;

    roomInfo.style.display = "flex";
})

const usernameInp = document.getElementById('usernameInput');
const usernameBtn = document.getElementById('createUsernameBtn');
const spanUsername = document.getElementById('username');

usernameBtn.addEventListener('click', () => {

    const username = usernameInp.value
    if (username.trim() === "") return;

    spanUsername.innerText = username;

    localStorage.setItem("username", username);
})

const entranceBtn = document.getElementById('entranceBtn');
const entranceID = document.getElementById('entranceID');
const errorP = document.getElementById('errorP');

entranceBtn.addEventListener('click', async () => {

    const roomId = entranceID.value.trim();
    if (roomId === "") {
        errorP.innerText = "Введите ID комнаты";
        return;
    }
    const response = await fetch(`/check_room/${entranceID.value}`);
    const data = await response.json();

    if (data.error === 0) {
        window.location.href = data.link
    } else if (data.error === 1) {
        errorP.innerText = 'Комнаты не существует'
    }
})
