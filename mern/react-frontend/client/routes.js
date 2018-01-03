// import React from 'react'
// import { Router, Route } from 'react-router-dom'
// import App from './components/app'
// import Product from './pages/product'
//
// export const Routes = () => (
//   <Router>
//     <div>
//       <Route exact path='/' component={App}/>
//       <Route path='/product' component={Product}/>
//     </div>
//   </Router>
// )


import React from 'react';
import { Route, Switch } from 'react-router-dom';
import App from './components/app';
import Product from './pages/product'

export const Routes = () => (
  <Switch>
    <Route exact path='/' component={App} />
    <Route path='/product' component={Product}/>
  </Switch>
);
export default Routes;