function openInfo() {
    let box = document.getElementById("more-info-box");
    if (box.style.zIndex == 1 || box.style.opacity == 1) {
        return
    }
    if (currentThread.type == "group") {
        let title = document.createElement("h4");
        title.innerHTML = "members";
        box.appendChild(title);
        let membersList = document.createElement("div");
        membersList.id = "members-list";
        box.appendChild(membersList);
        let currentGroup = grouplist.find(function(d) {
            return d.name == currentThread.name;
        })
        // let membersList = document.getElementById("members-list");
        currentGroup.members.forEach(function(n){
            let tab = document.createElement("div");
            tab.innerHTML = n;
            membersList.appendChild(tab);
        })
    }
    box.style.opacity = 1;
    box.style.zIndex = 1;
}

document.getElementById("main-box").addEventListener("click", function (event) {
    if (!(document.getElementById("more-info-box").contains(event.target) 
    || event.target == document.getElementById("more-info-button"))) {
        closeInfo();
    }
    // console.log(event.target)
    if (!(document.getElementById("emoji-box").contains(event.target) 
    || document.getElementById("emoji-button").contains(event.target))) {
        closeEmoji();
    }
});


function closeInfo() {
    let box = document.getElementById("more-info-box");
    box.innerHTML = "";
    if (box.style.zIndex == -1 || box.style.opacity == 0) return;

    box.style.opacity = 0;
    setTimeout(function () {
        box.style.zIndex = -1;
    }, 500);
}

function openEmoji() {
    let box = document.getElementById("emoji-box");
    if (box.style.zIndex == 1 || box.style.opacity == 1) {
        return
    }
    console.log(box.hasChildNodes())
    if (!box.hasChildNodes()) {
        let emojiList = getAllEmoji();
        emojiList.forEach(function(e) {
            let choice = document.createElement("div");
            choice.className = "emoji-cell";
            choice.innerHTML = e;
            choice.setAttribute("onclick", "chooseEmoji(this)");
            box.appendChild(choice);
        })
    }
    box.style.opacity = 1;
    box.style.zIndex = 1;
}

function chooseEmoji(node) {
    console.log(node.innerHTML);
    let textarea = document.getElementById("myMessage");
    insertAtCursor(textarea, node.innerHTML);
}

function closeEmoji () {
    let box = document.getElementById("emoji-box");
    // box.innerHTML = "";
    if (box.style.zIndex == -1 || box.style.opacity == 0) return;

    box.style.opacity = 0;
    setTimeout(function () {
        box.style.zIndex = -1;
    }, 500);
}



function openBox() {
    let box = document.getElementById("selection-box");
    if (box.style.zIndex == 1 || box.style.opacity == 1) {
        return;
    }

    let userCheckbox = document.getElementById("users-checkbox");
    updateUserList();
    otherUsers.forEach(function (d) {
        let input = document.createElement("input");
        input.type = "checkbox";
        input.name = d.name;
        input.id = d.name + "-input";
        let label = document.createElement("label");
        label.innerHTML = d.name;
        userCheckbox.appendChild(input);
        userCheckbox.appendChild(label);
        userCheckbox.appendChild(document.createElement("br"));
    });

    box.style.opacity = 1;
    box.style.zIndex = 1;
}

function createRoom() {
    function checkExistence(n) {
        for (let i = 0; i < grouplist.length; i++) {
            if (grouplist[i].name == n) {
                return true;
            }
        }
        return false;
    }
    let checkBoxes = document.querySelectorAll("#users-checkbox input[type='checkbox']");
    console.log(checkBoxes);
    let selectedUsers = [];
    for (i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            selectedUsers.push(checkBoxes[i].name);
        }
    }
    console.log(selectedUsers);
    let groupName = $('#create-group-text').val();
    if (checkExistence(groupName)) {
        alert("group name exists!");
        $('#create-group-text').val('');
        return;
    } else {
        const createRoomMessage = {
            "Type": "Create", "Name": groupName, "From": currentUserName, "List": selectedUsers
        }
        socket.send(JSON.stringify(createRoomMessage));
        setTimeout(() => {
            updateGroupList(true, groupName);
        }, 500);
        changeColor();
    }
    closeBox();
}

function closeBox() {
    let box = document.getElementById("selection-box");

    box.style.opacity = 0;
    setTimeout(function () {
        box.style.zIndex = -1;
        let userCheckbox = document.getElementById("users-checkbox");
        userCheckbox.innerHTML = "";
        $('#create-group-text').val('');
    }, 500);

}


function changeColor() {
    let chordAudio = document.getElementById("chord-audio");
    chordAudio.play();
    document.body.style.backgroundColor = `hsl(${Math.random() * 360}, 60%, 60%)`;
}


function getAllEmoji() {
    let L = [];
    let start = 0x1f600;
    for (let i = start; i < start + 80; i++) {
        L.push(String.fromCodePoint(i));
    }
    return L;
}

function insertAtCursor(myField, myValue) {
    //IE support
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
    }
    //MOZILLA and others
    else if (myField.selectionStart || myField.selectionStart == '0') {
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;
        myField.value = myField.value.substring(0, startPos)
            + myValue
            + myField.value.substring(endPos, myField.value.length);
    } else {
        myField.value += myValue;
    }
}