let ws = new WebSocket("ws://localhost:5000/game");

const list = document.getElementsByClassName("tile");
for (let element of list) {
	element.addEventListener("click", () => {if (!finished) {ws.send(element.id.toString())}});
}

ws.onopen = function (event) {
    ws.send("new");
    finished = false
};

ws.onmessage = function (event) {
	data = JSON.parse(event.data);
    console.log("message " + data)
	for (i = 0; i < 9; i++) {
		document.getElementById(i.toString()).innerHTML = ox(data["board"][i])
	}
	if (data.result == "won") {
		finished = true
		document.getElementById("status").innerHTML = "Partie finie"
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