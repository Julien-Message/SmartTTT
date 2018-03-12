let ws = new WebSocket("ws://localhost:5000/new-game");

const list = document.getElementsByClassName("tile");
for (let element of list) {
	element.addEventListener("click", () => ws.send(element.id.toString()));
}

ws.onopen = function (event) {
    console.log("open")
    ws.send("new");
};

ws.onmessage = function (event) {
	data = JSON.parse(event.data);
    console.log("message " + data)
	for (i = 0; i < 9; i++) {
		console.log(i)
		console.log(data["board"])
		document.getElementById(i.toString()).innerHTML = ox(data["board"][i])
	}
};

ws.onclose = function (event) {
    console.log("close")
};

ox = function(tile) {
	if (tile == "blank") {
		return "";
	}
	if (tile == "cross") {
		return "X";
	}
	if (tile == "circle") {
		return "O";
	}
}