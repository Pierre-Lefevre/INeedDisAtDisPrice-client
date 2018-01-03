import { Products } from '../../api/products/products';

import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
  // code to run on server at startup
  console.log(Products.find().count())
});
