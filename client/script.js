let ws = new WebSocket("ws://localhost:5000/game");

const list = document.getElementsByClassName("tile");
for (let element of list) {
	element.addEventListener("click", () => {
		if (!finished) {
			console.log(JSON.stringify(element))
			ws.send(element.id.toString())
		}
	});
}

newGame = function(){
	console.log("new game");
	ws.send("new");
	finished = false;
}

ws.onopen = function (event) {
    newGame();
};

ws.onmessage = function (event) {
	data = JSON.parse(event.data);
    console.log("message " + JSON.stringify(data))
	for (i = 0; i < 9; i++) {
		document.getElementById(i.toString()).innerHTML = ox(data["board"][i])
	}
	console.log(data.result)
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