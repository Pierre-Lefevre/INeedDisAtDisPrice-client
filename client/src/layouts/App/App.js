import React from 'react'
import { Router, Route } from 'react-router-dom'
import Navigation from '../../components/Navigation/Navigation'
import Products from '../../pages/Products/Products'
import Product from '../../pages/Product/Product'
import Profile from '../../pages/Profile/Profile'

import Auth from '../../modules/Auth/Auth.js'
import Callback from '../../modules/Callback/Callback'
import history from '../../modules/history'

const auth = new Auth()

const handleAuthentication = (nextState, replace) => {
  if (/access_token|id_token|error/.test(nextState.location.hash)) {
    auth.handleAuthentication()
  }
}

const App = () => (
  <Router history={history}>
    <div>
      <Navigation auth={auth} {...this.props} />
      <Route exact path="/" component={Products}/>
      <Route path="/products" component={Products}/>
      <Route path="/product/:id" component={Product}/>
      <Route path="/callback" render={(props) => {
        handleAuthentication(props)
        return <Callback {...props} />
      }}/>
      <Route path="/profile" render={(props) => {
        handleAuthentication(props)
        return <Profile auth={auth} {...props} />
      }}/>
    </div>
  </Router>
)

export default App
