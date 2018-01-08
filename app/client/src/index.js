import React from 'react'
import ReactDOM from 'react-dom'
import registerServiceWorker from './registerServiceWorker'
import App from './layouts/App/App'
import { IntlProvider } from 'react-intl'
import { addLocaleData } from 'react-intl'
import frLocaleData from 'react-intl/locale-data/fr'

import './stylesheets/app.css'

addLocaleData(frLocaleData)

ReactDOM.render(<IntlProvider locale="fr"><App/></IntlProvider>, document.getElementById('root'))
registerServiceWorker()
