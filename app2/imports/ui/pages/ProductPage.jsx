import React from 'react';
import PropTypes from 'prop-types'

export default class ProductPage extends React.Component {
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
    const { product } = this.props;


    return (
      <div>{product.name}</div>
    );
  }
}

ProductPage.propTypes = {
  // user: React.PropTypes.object,      // current meteor user
  // connected: React.PropTypes.bool,   // server connection status
  // loading: React.PropTypes.bool,     // subscription status
  // menuOpen: React.PropTypes.bool,    // is side menu open?
  product: PropTypes.array,      // all lists visible to the current user
  // children: React.PropTypes.element, // matched child route component
  // location: React.PropTypes.object,  // current router location
  // params: React.PropTypes.object,    // parameters of the current route
};