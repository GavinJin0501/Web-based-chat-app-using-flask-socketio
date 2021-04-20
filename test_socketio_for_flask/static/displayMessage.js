console.log("works");

function appendMessageFromJSON(message) {
    console.log(message);
    let messageElement = document.createElement("div");
    messageElement.className = "message-element";

    let title = document.createElement("p");
    title.className = "message-element-title";

    let name = document.createElement("span");
    name.className = "message-element-name";
    name.innerHTML = message.From;
    title.appendChild(name);

    let time = document.createElement("span");
    time.className = "message-element-time";
    if (message.Time) {
        time.innerHTML = message.Time;
    } else{
        time.innerHTML = moment().format("YYYY-MM-DD hh:mm:ss");
    }
    
    title.appendChild(time);

    messageElement.appendChild(title);
    
    
    let content = document.createElement("p");
    if (message.From == currentUserName) {
        content.className = "message-element-content-mine";
    } else{
        content.className = "message-element-content";
    }
    
    if(message.is_image == 0) {
        content.innerHTML = message.Content;
    }else{
        let img = document.createElement("img");
        img.src = message.Content;
        img.className = "content-image"
        content.appendChild(img);
    }
    

    messageElement.appendChild(content);
    return messageElement; // return a html node
}

