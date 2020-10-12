'use strict';

var os = require('os');
var nodeStatic = require('node-static');
var http = require('http');
var url = require('url')
var fs = require('fs')
var querystring=require("querystring");


var fileServer = new(nodeStatic.Server)();



//서버 시작 
var app = http.createServer(function(request, response) {
  
  //서버가 만들어지면 파일서버가 작동함 
  fileServer.serve(request, response);
  var pathname = url.parse(request.url).pathname;
  if (pathname=="/" || pathname==""){
    console.log("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE");
    
  }
  else if(pathname=="/save"){
    if (request.method=="POST"){
      let body = [];
      request.on('data', (chunk) => {
        body.push(chunk);
      }).on('end', () => {
        body = Buffer.concat(body).toString();
        var data = querystring.parse(body);
      
        console.log("id " + data["id"]);
        console.log("pwd " + data['pwd']);
        var img = data['img'];
        //img = img.replace(/^data:image\/\w+;base64,/, "");
        //img = img.replace(" ", "+")
        img = img.replace('data:image/png;base64,', '');
        img = img.replace(' ', '+')
        console.log(img)
    
        var buff =  Buffer.from(img, 'base64');
        console.log(buff)
        fs.writeFileSync('aaa.png', buff);
      });
       
        console.log("요청받음")
    }
  }

}).listen(8080, function(){
	console.log("server start at 8080");
});


