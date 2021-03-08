var http = require('http');

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end('Hello World!');
}).listen(8080);

// 一个特别特别简单的测试 https://www.w3schools.com/nodejs/default.asp