const express = require('express');

app = express()
let data = null

app.post('/receive', (req, res) =>{

    res.contentType('application/json')

    data = req.body
    res.status(201).send(data)
})

app.get('/response', (req, res) => {

    res.contentType('application/json')
    res.status(200).send(data)
    
})
