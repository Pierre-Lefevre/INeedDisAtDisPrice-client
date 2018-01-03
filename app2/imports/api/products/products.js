import { Mongo } from 'meteor/mongo';

class ProductsCollection extends Mongo.Collection {

}

export const Products = new ProductsCollection('products');
