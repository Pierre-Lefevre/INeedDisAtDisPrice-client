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
    const { loading, product } = this.props;
console.log("aa" + loading)

    return (
      loading ? "" : <div>{product.name}</div>
    );
  }
}

ProductPage.propTypes = {
  // user: React.PropTypes.object,      // current meteor user
  // connected: React.PropTypes.bool,   // server connection status
  loading: PropTypes.bool,
  // menuOpen: React.PropTypes.bool,    // is side menu open?
  product: PropTypes.object,      // all lists visible to the current user
  // children: React.PropTypes.element, // matched child route component
  // location: React.PropTypes.object,  // current router location
  // params: React.PropTypes.object,    // parameters of the current route
};