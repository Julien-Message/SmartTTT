var ws = new WebSocket("ws://localhost:5000");

ws.onopen = function (event) {
    console.log("open")
    ws.send('{ "type": "texte", "message": "Prêt" }' );
};

ws.onmessage = function (event) {
    console.log("message")
    var data = JSON.parse(event.data);
    console.log(data.message)
};

ws.onclose = function (event) {
    console.log("close")
};