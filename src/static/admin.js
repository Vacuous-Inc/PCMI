
const socket = io("/admin");

socket.on("connect", function() {
  console.log(socket.id); // x8WIv7-mJelg7on_ALbx
});

var startButton = $("#start");
startButton.click(function(){
    console.log("button pressed")
    socket.emit("start_game")
});

socket.on("started", function() {
    console.log("started")
    startButton.text("End Game")
});