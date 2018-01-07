//====LIST DEPENDENCIES===//

const express = require('express');
const parseurl = require('parseurl');
const bodyParser = require('body-parser');
const path = require('path');
const expressValidator = require('express-validator');
const mongoose = require('mongoose');
const Signature = require('./models/signature.js')
const Products = require('./models/Products.js')
const app = express();
var cors = require('cors');
const url = 'mongodb://localhost:27017/iNeedDisAtDisPrice';
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
//=========================//

app.use(cors());

//====ROOT DIRECTORY===//

app.get('/', function(req, res) {
  res.json('you did it');
});

//==========================//

//====GET ALL SIGNATURES===//

app.get('/api/products', function(req, res) {
  Products.find({}).then(eachOne => {
    res.json(eachOne);
    })
  })

app.get('/api/product/:id', function(req, res) {
	console.log(req.params.id)
  Products.findOne({_id:req.params.id}).then(eachOne => {
    res.json(eachOne);
    })
  })


//==========================//

//====POST NEW SIGNATURE===//

app.post('/api/signatures', function(req, res) {
console.log(req.query)
  Signature.create({
    guestSignature: req.query.SignatureOfGuest,
    message: req.query.MessageofGuest,
  }).then(signature => {
    res.json(signature)
  });
});

//==========================//

//====MONGOOSE CONNECT===//

mongoose.connect(url, function (err, db) {
 if (err) {
   console.log('Unable to connect to the mongoDB server. Error:', err);
 } else {
   console.log('Connection established to', url);
 }
});

app.listen(3333, function () {
  console.log('Example app listening on port 3000!')
})

//==========================//