var mongoose = require('mongoose')
var Schema = mongoose.Schema

var expenseSchema = new Schema({
  store: String,
  name: String
})

module.exports = mongoose.model('Product', expenseSchema)