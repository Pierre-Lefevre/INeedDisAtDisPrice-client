import React from 'react'
import ReactDOM from 'react-dom'
import registerServiceWorker from './registerServiceWorker'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import ProductsList from './ProductsList'
import ViewProduct from './ViewProduct'
import { IntlProvider } from 'react-intl'
import { addLocaleData } from 'react-intl'
import frLocaleData from 'react-intl/locale-data/fr'

import './index.css'

addLocaleData(frLocaleData)

ReactDOM.render(
  <IntlProvider locale="fr">
    <Router>
      <Switch>
        <Route exact name="index" path="/" component={ProductsList}/>
        <Route exact path="/:id" component={ViewProduct}/>
      </Switch>
    </Router>
  </IntlProvider>, document.getElementById('root'))
registerServiceWorker()
