import { Meteor } from 'meteor/meteor'
import { withTracker } from 'meteor/react-meteor-data'
import { Products } from '../../api/products/products.js'
import App from '../layouts/App.jsx'

export default ListPageContainer = withTracker(() => {
  const subscription = Meteor.subscribe('products.list')
  const loading = !subscription.ready()
  const products = Products.find().fetch()

  return {
    loading,
    products
  }
})(App)
