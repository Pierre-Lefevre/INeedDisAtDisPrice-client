import React from 'react';
import { render } from 'react-dom';
import { Meteor } from 'meteor/meteor';
import App from '../../ui/layouts/App/App';
import '../both/api';
import { IntlProvider } from 'react-intl';

import '../../ui/stylesheets/app.scss';

Meteor.startup(() => render(<IntlProvider locale="fr"><App /></IntlProvider>, document.getElementById('react-root')));
