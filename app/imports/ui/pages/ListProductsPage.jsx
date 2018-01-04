import React from 'react';
import PropTypes from 'prop-types'
import ProductItem from '../components/ProductItem.jsx';

export default class ListProductsPage extends React.Component {
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
    const { loading, products } = this.props;

    if (!loading) {
      let Products = products.map(product => (
        <ProductItem
          product={product}
          key={product._id}
        />
      ));
      return (
        Products
      );
    }


    return (
      ""
    );
  }
}

ListProductsPage.propTypes = {
  // user: React.PropTypes.object,      // current meteor user
  // connected: React.PropTypes.bool,   // server connection status
  loading: PropTypes.bool,
  // menuOpen: React.PropTypes.bool,    // is side menu open?
  products: PropTypes.array,      // all lists visible to the current user
  // children: React.PropTypes.element, // matched child route component
  // location: React.PropTypes.object,  // current router location
  // params: React.PropTypes.object,    // parameters of the current route
};