import { Meteor } from 'meteor/meteor';
import { Products } from '../../api/products/products.js';
import { withTracker } from 'meteor/react-meteor-data';
import App from '../layouts/App.jsx';

export default ListPageContainer = withTracker(() => {
  // const todosHandle = Meteor.subscribe('todos.inList', id);
  // const loading = !todosHandle.ready();
  const products = Products.find().fetch();
  // const listExists = !loading && !!list;
  return {
    // loading,
    products,
    // listExists,
    // todos: listExists ? list.todos().fetch() : [],
  };
})(App);
