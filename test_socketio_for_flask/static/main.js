var otherUsers = [];
var grouplist = [];
var currentThread;

$(document).ready(function () {
    var socket = io.connect('http://127.0.0.1:5000');
    updateUserList();
    updateGroupList();
    // requesting the server to update groupchat and user list
    setInterval(updateUserList, 20000);
    setInterval(updateGroupList, 20000);

    socket.on('connect', function () {
        const meInfo = { "Type": "Connect", "Id": socket.id, "Username": currentUserName }
        socket.send(JSON.stringify(meInfo));
    });

    socket.on('message', function (msg) {
        var temp;
        msg = JSON.parse(msg);
        // console.log(msg);
        // appendMessageFromJSON(msg);
        if (msg.Type == "Connect") {
            temp = msg.Time.concat(" ", msg.Username, ": ", msg.Content);
            // $("#messages").append('<li>' + temp + '</li>');
        } else if (msg.Type == "Send") {
            document.getElementById("message-box").appendChild(appendMessageFromJSON(msg));
            // temp = msg.Time.concat(" ", msg.From, ": ", msg.Content);
            // $("#messages").append('<li>' + temp + '</li>');
        } else if (msg.Type == "history") {
            console.log("Receive history");
            // msg.Content.forEach(element => $("#messages").append('<li>' + element + '</li>'));
        }

        console.log('Received message');
    });

    // sending the messages using the button or the enter key
    $('#sendbutton').on('click', sendMessage);
    $('#myMessage').on('keypress', function (e) {
        if (e.which == 13 || e.keyCode == 13) {
            sendMessage();
        }
    });


    function sendMessage() {
        console.log('Send message');
        msg = $('#myMessage').val();
        // $("#messages").append('<li>' + msg + '</li>');
        // only sends to the currentThread 周四晚上排练前写的 没写完的功能
        const meInfo = { "Type": "Send", "From": currentUserName, "To": currentThread, "Content": msg, "Chat": "group"};
        document.getElementById("message-box").appendChild(appendMessageFromJSON(meInfo));
        socket.send(JSON.stringify(meInfo));
        $('#myMessage').val('');
    }
});
// testing logging out by closing the tab
window.addEventListener("beforeunload", function (e) {
    $.ajax({
        url: "/logout/{{username}}",
        type: "GET"
    })
    return;
});

function selectBar(node) {
    if (node.id == "selected-sidebar") return;
    
    if (document.getElementById("selected-sidebar") != null) {
        document.getElementById("selected-sidebar").setAttribute("id", "");
    };
    node.setAttribute('id', "selected-sidebar");
    currentThread = node.firstChild.innerHTML;
    console.log(currentThread)
}

function updateUserList() {
    $.ajax({
        url: "/get-user-list",
        type: "POST",
        dataType: "json",
        success: function (data) {
            console.log("users:",data.userlist);
            function checkExistence(username) {
                for (let i = 0; i < otherUsers.length; i++) {
                    if (otherUsers[i].name == username) {
                        return true;
                    }
                    return false;
                }
            }
            let removingUsers = otherUsers.filter(u => !data.userlist.includes(u.name));
            removingUsers.forEach(function (u) {
                // let removingChild = document.getElementById(u + "-user-element");
                document.getElementById("all-active-users-box").removeChild(u.node);
            });
            otherUsers = otherUsers.filter(u => data.userlist.includes(u.name));
            data.userlist.forEach(function (u) {
                if (u == currentUserName || checkExistence(u)) {
                    return;
                }
                else if (!checkExistence(u)) {
                    let userTab = document.createElement('div');
                    userTab.className = 'sidebar-element';
                    // userTab.id = u + "-user-element";
                    userTab.setAttribute("onclick", "selectBar(this)");
                    let displayedUsername = document.createElement('h4');
                    displayedUsername.className = 'sidebar-element-name';
                    displayedUsername.innerHTML = u;
                    document.getElementById("all-active-users-box").appendChild(userTab);
                    userTab.appendChild(displayedUsername);
                    otherUsers.push({ "name": u, "node": userTab });
                }

            });
        }
    })
}

function updateGroupList() {
    $.ajax({
        url: "/get-group-list",
        type: "POST",
        dataType: "json",
        success: function (data) {
            console.log("groups:", data.grouplist);
            function checkExistence(groupname) {
                for (let i = 0; i < grouplist.length; i++) {
                    if (grouplist[i].name == groupname) {
                        return true;
                    }
                    return false;
                }
            }
            for (const [key, value] of Object.entries(data.grouplist)) {
                if (checkExistence(key)) {
                    continue;
                } else {
                    let groupTab = document.createElement('div');
                    groupTab.className = 'sidebar-element';
                    // groupTab.id = key + "-group-element";
                    groupTab.setAttribute("onclick", "selectBar(this)");
                    let displayedGroupName = document.createElement('h4');
                    displayedGroupName.className = 'sidebar-element-name';
                    displayedGroupName.innerHTML = key;
                    document.getElementById("all-groups-box").appendChild(groupTab);
                    groupTab.appendChild(displayedGroupName);
                    grouplist.push({ "name": key, "node": groupTab });
                }
            }
        }
    })
}