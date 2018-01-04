import { Meteor } from 'meteor/meteor'
import { Mongo } from 'meteor/mongo'
import { withTracker } from 'meteor/react-meteor-data'
import { Products } from '../../api/products/products.js'
import ProductPage from '../pages/ProductPage.jsx'

export default ProductContainer = withTracker((props) => {
  const subscription = Meteor.subscribe('products.view', props.match.params.id)
  const loading = !subscription.ready()
  const product = Products.findOne({_id: new Mongo.ObjectID(props.match.params.id)})

  return {
    loading,
    product
  }
})(ProductPage)
