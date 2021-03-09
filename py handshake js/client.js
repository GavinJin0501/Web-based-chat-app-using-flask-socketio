const net = require('net');
const client = net.createConnection({ port: 12000}, () => {
    console.log("Client: I connected to the server.");
    client.write("Client: Hello this is client!");
});

client.on('data', (data) => {
    console.log(data.toString());
    client.end();
});

client.on('end', () => {
    console.log("Client: I disconnected from the server.")
})