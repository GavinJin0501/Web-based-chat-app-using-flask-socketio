var otherUsers = []; // [{name: xxx, node: js DOM element}, {}]
var grouplist = []; // [{name: xxx, node: js DOM element}, {}]
var currentThread = {
    name: undefined,
    type: undefined // group/private
};
var defaultThread;
var socket;



$(document).ready(function () {
    socket = io.connect('http://127.0.0.1:5000');
    
    function handleFileSelect(ele) {
        console.log("handled")
        var file = ele.target.files[0];
        var fileReader = new FileReader();
        fileReader.readAsDataURL(file);
        fileReader.onload = () => {
            var arrayBuffer = fileReader.result;
            const msg = {
                Type: "Send",
                From: currentUserName,
                To: currentThread.name,
                Chat: currentThread.type,
                Content: arrayBuffer,
                is_image: 1
            };
            let messageElement = appendMessageFromJSON(msg);
            document.getElementById("message-box").appendChild(messageElement);
            messageElement.scrollIntoView();
            socket.send(JSON.stringify(msg));
            console.log(file.size);
            // console.log(fileReader.result);
        }
    }

    document.getElementById("file-uploader").addEventListener("change", handleFileSelect, false);

    updateUserList();

    // javascript的async结构太复杂了，
    // 简单粗暴的解决方法，第一次运行updateGroupList的时候
    // 输入一个true，在函数内部的ajax实现selectBar给general的功能
    updateGroupList(true, "general");
    // requesting the server to update groupchat and user list
    setInterval(updateUserList, 5000);
    setInterval(updateGroupList, 5000);

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
            console.log(msg);
            function incrementUnread(obj) {
                if (obj.unreadNum == 0) {
                    obj.unreadNum++;
                    let icon = document.createElement("p");
                    icon.className = "sidebar-element-unread-icon";
                    icon.innerHTML = obj.unreadNum;
                    obj.node.appendChild(icon);
                }
                else if (obj.unreadNum > 0) {
                    obj.unreadNum++;
                    let icon = obj.node.children[1];
                    icon.innerHTML = obj.unreadNum;
                }
            }
            if (msg.Chat == "group") {
                if (msg.To == currentThread.name) {
                    let messageElement = appendMessageFromJSON(msg);
                    document.getElementById("message-box").appendChild(messageElement);
                    messageElement.scrollIntoView();
                    // document.getElementById("message-box").appendChild(appendMessageFromJSON(msg));
                } 
                else {
                    document.getElementById("drip-audio").play();
                    let targetThread = grouplist.find(obj => obj.name == msg.To);
                    incrementUnread(targetThread);
                }
            }
            else if (msg.Chat == "private") {
                if (msg.From == currentThread.name) {
                    let messageElement = appendMessageFromJSON(msg);
                    document.getElementById("message-box").appendChild(messageElement);
                    messageElement.scrollIntoView();
                    // document.getElementById("message-box").appendChild(appendMessageFromJSON(msg));
                }
                else {
                    document.getElementById("drip-audio").play();
                    let targetThread = otherUsers.find(obj => obj.name == msg.From);
                    incrementUnread(targetThread);
                }
            }
            // temp = msg.Time.concat(" ", msg.From, ": ", msg.Content);
            // $("#messages").append('<li>' + temp + '</li>');
        } else if (msg.Type == "history") {
            console.log("Receive history");
            console.log(msg);
            msg.Content.forEach(function (element, i) {
                // 收到history的tuple
                let jsonMsg = {
                    Time: element[1],
                    From: element[0],
                    Content: element[2] || element[3],
                    is_image: element[2] ? 0 : 1
                }
                document.getElementById("message-box").appendChild(appendMessageFromJSON(jsonMsg));
            });
            document.getElementById("message-box").lastChild.scrollIntoView();
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
        if (msg.length == 0) {
            alert("No empty message.")
            return;
        }
        if (/\p{Extended_Pictographic}/u.test(msg)) {
            changeColor();
        }
        // $("#messages").append('<li>' + msg + '</li>');
        // only sends to the currentThread 周四晚上排练前写的 没写完的功能
        const meInfo = {
            "Type": "Send", "From": currentUserName,
            "To": currentThread.name, "Content": msg, "Chat": currentThread.type, "is_image": 0
        };
        // 在UI上显示自己发的信息
        let messageElement = appendMessageFromJSON(meInfo);
        document.getElementById("message-box").appendChild(messageElement);
        messageElement.scrollIntoView();
        socket.send(JSON.stringify(meInfo));
        $('#myMessage').val("");
    }
});
// testing logging out by closing the tab
window.addEventListener("beforeunload", function (e) {
    $.ajax({
        url: "/logout/" + currentUserName,
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
    document.getElementById("message-box").innerHTML = "";
    
    if (node.children.length > 1 ) {
        node.removeChild(node.children[1]);
    }
    

    currentThread.name = node.firstChild.innerHTML;
    let parentID = node.parentNode.id;
    let targetThread;
    if (parentID == "all-groups-box") {
        currentThread.type = "group";
        targetThread = grouplist.find(obj => obj.name == currentThread.name);
        if (targetThread) {
            targetThread.unreadNum = 0;
        }
    } else if (parentID == "all-active-users-box") {
        currentThread.type = "private";
        targetThread = otherUsers.find(obj => obj.name == currentThread.name);
        if (targetThread) {
            targetThread.unreadNum = 0;
        }
    }
    const joinMsg = {
        "Type": "Join", "From": currentUserName,
        "To": currentThread.name, "Chat": currentThread.type
    }
    socket.send(JSON.stringify(joinMsg));
    console.log(currentThread)
}

function updateUserList() {
    $.ajax({
        url: "/get-user-list",
        type: "POST",
        dataType: "json",
        success: function (data) {
            console.log("users:", data.userlist);
            function checkExistence(username) {
                for (let i = 0; i < otherUsers.length; i++) {
                    if (otherUsers[i].name == username) {
                        return true;
                    }    
                }
                return false;
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
                    otherUsers.push({ "name": u, "node": userTab, "unreadNum": 0});
                }

            });
        }
    })
}

function updateGroupList(select, name) {
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
                }
                return false;
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
                    if (select && key == name) {
                        selectBar(groupTab);
                    }
                    grouplist.push({ "name": key, "node": groupTab, "unreadNum": 0, "members": value});
                }
            }
        }
    })
}