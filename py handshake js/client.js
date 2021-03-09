const net = require('net');
const server_port = 12000;
const server_name = "172.20.10.6"

const client = net.createConnection(server_port, server_name, () => {
    console.log("CLIENT: I connected to the server.");
    client.write("CLIENT: Hello this is client!");
});

client.on('data', (data) => {
    console.log(data.toString());
    client.end();
});

client.on('end', () => {
    console.log("CLIENT: I disconnected from the server.")
})