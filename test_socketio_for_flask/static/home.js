console.log("external");

$(document).ready(function() {
	var socket = io.connect('http://127.0.0.1:5000');
    var currentUserName;

    // get username using ajax
    $.ajax({
        url: "/getMyInfo",
        type: "POST",
        dataType: "json",
        success: (data) => {
            currentUserName = data.username;
            console.log(currentUserName);
        }
    })
    
	socket.on('connect', function() {
			const meInfo = {"Type": "Socket", "Id": socket.id, "Username": currentUserName}
		    socket.send(JSON.stringify(meInfo));
	});

	socket.on('message', function(msg) {
		$("#messages").append('<li>'+msg+'</li>');
		console.log('Received message');
	});

	$('#sendbutton').on('click', function() {
        console.log('Send message');
	    const meInfo = {"Type": "Post", "From": currentUserName, "To": "broadcast", "Content": $('#myMessage').val()};
		socket.send(JSON.stringify(meInfo));
		$('#myMessage').val('');
	});
});