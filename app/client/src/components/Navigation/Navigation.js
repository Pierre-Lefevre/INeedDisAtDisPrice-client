import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
// import PublicNavigation from '../PublicNavigation/PublicNavigation';
// import AuthenticatedNavigation from '../AuthenticatedNavigation/AuthenticatedNavigation';

import './Navigation.css';

const Navigation = props => (
  <nav>
    <div id="brand">
      <Link to="/">I Need Dis At Dis Price</Link>
    </div>
    <ul id="menu">
      <li><Link to="/">Produits</Link></li>
    </ul>
    {/*{!props.authenticated ? <PublicNavigation /> : <AuthenticatedNavigation {...props} />}*/}
  </nav>
);

Navigation.defaultProps = {
  name: '',
};

Navigation.propTypes = {
  authenticated: PropTypes.bool.isRequired,
  name: PropTypes.string,
};

export default Navigation;
