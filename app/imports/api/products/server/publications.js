import { Meteor } from 'meteor/meteor'
import { Mongo } from 'meteor/mongo'
import { check } from 'meteor/check'
import { Products } from '../products'

Meteor.publish('products.list', () => Products.find())

Meteor.publish('products.view', (_id) => {
  check(_id, String)
  return Products.find({_id: new Mongo.ObjectID(_id)})
})