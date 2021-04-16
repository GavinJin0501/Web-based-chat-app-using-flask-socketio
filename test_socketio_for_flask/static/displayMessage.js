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
    time.innerHTML = message.Time;
    title.appendChild(time);

    messageElement.appendChild(title);

    let content = document.createElement("p");
    content.className = "message-element-content";
    content.innerHTML = message.Content;

    messageElement.appendChild(content);
    return messageElement; // return a html node
}

