import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Products from '../../pages/Products/Products'
import Product from '../../pages/Product/Product'

const App = () => (
  <Router>
    <Switch>
      <Route exact name="products" path="/" component={Products}/>
      <Route exact name="product" path="/:id" component={Product}/>
    </Switch>
  </Router>
)

export default App
