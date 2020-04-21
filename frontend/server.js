const express = require('express')
const server = express()

server.get('/static/*', (req, res) => {
    res.sendFile(`static/${req.params[0]}`, {root: './dist/'})
})

server.get('/*', (req, res) => {
    res.sendFile('index.html', {root: './dist/'})
})

const port = 5000;
server.listen(port, function() {
    console.log('server listening on port ' + port)
})
