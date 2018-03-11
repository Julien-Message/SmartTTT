var ws = new WebSocket("ws://localhost:5000");

ws.onopen = function (event) {
    console.log("open")
    ws.send("new");
};

ws.onmessage = function (event) {
    console.log("message")
    console.log(event.data)
};

ws.onclose = function (event) {
    console.log("close")
};