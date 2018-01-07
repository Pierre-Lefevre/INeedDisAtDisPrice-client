import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { Meteor } from 'meteor/meteor';
import { withTracker } from 'meteor/react-meteor-data';
import ProductsCollection from '../../../api/Products/Products';
import Loading from '../../components/Loading/Loading';
import { Table, Alert, Button } from 'react-bootstrap';
import currencyUtils from '../../../modules/currency-utils';

import './Products.scss';

const Products = ({ loading, products, match, history }) =>
  !loading ? (
    <div>
      {products.length ? (
        <ul id="products-list">
          {products.map(({ _id, name, image_name, price, currency }) => (
            <li key={_id}>
              <Link to={match.url + '/' + _id}>
                <figure>
                  <img src={'/img/products/' + image_name + '.jpg'} alt={name} />
                  <figcaption>
                    <div className="product-name">{name}</div>
                    <div className="product-price">
                      {price.toFixed(2)} {currencyUtils.codeToSymbol(currency)}
                    </div>
                  </figcaption>
                </figure>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <Alert bsStyle="warning">No documents yet!</Alert>
      )}
    </div>
  ) : (
    <Loading />
  );

Products.propTypes = {
  loading: PropTypes.bool.isRequired,
  products: PropTypes.arrayOf(PropTypes.object).isRequired,
  match: PropTypes.object.isRequired,
  history: PropTypes.object.isRequired,
};

export default withTracker(() => {
  const subscription = Meteor.subscribe('products');
  return {
    loading: !subscription.ready(),
    products: ProductsCollection.find().fetch(),
  };
})(Products);
