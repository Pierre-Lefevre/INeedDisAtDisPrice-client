import React from 'react';
import PropTypes from 'prop-types'
import ListProductsPage from '../pages/ListProductsPage';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    // this.state = {
    //   menuOpen: false,
    //   showConnectionIssue: false,
    // };
    // this.toggleMenu = this.toggleMenu.bind(this);
    // this.logout = this.logout.bind(this);
  }

  render() {
    const { products } = this.props;

    return (
      <ListProductsPage products={products} />
    );
  }
}

App.propTypes = {
  // user: React.PropTypes.object,      // current meteor user
  // connected: React.PropTypes.bool,   // server connection status
  // loading: React.PropTypes.bool,     // subscription status
  // menuOpen: React.PropTypes.bool,    // is side menu open?
  products: PropTypes.array,      // all lists visible to the current user
  // children: React.PropTypes.element, // matched child route component
  // location: React.PropTypes.object,  // current router location
  // params: React.PropTypes.object,    // parameters of the current route
};