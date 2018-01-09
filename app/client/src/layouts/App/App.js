import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Navigation from '../../components/Navigation/Navigation'
import Products from '../../pages/Products/Products'
import Product from '../../pages/Product/Product'

const App = () => (
  <Router>
    <div>
      <Navigation/>
      <Switch>
        <Route exact name="products" path="/" component={Products}/>
        <Route exact name="product" path="/:id" component={Product}/>
      </Switch>
    </div>
  </Router>
)

export default App
