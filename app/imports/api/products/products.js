/* eslint-disable consistent-return */

import { Mongo } from 'meteor/mongo';
import SimpleSchema from 'simpl-schema';

const Products = new Mongo.Collection('products');

Products.allow({
  insert: () => false,
  update: () => false,
  remove: () => false,
});

Products.deny({
  insert: () => true,
  update: () => true,
  remove: () => true,
});

export default Products;
