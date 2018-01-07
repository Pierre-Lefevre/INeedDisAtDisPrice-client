import { Meteor } from 'meteor/meteor';
import { check } from 'meteor/check';
import Products from '../Products';

Meteor.publish('products', function documents() {
  return Products.find();
});

// Note: documents.view is also used when editing an existing document.
Meteor.publish('products.view', function documentsView(productId) {
  check(productId, String);
  return Products.find({ _id: new Mongo.ObjectID(productId) });
});
