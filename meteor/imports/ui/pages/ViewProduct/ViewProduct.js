import React from 'react';
import PropTypes from 'prop-types';
import { ButtonToolbar, ButtonGroup, Button } from 'react-bootstrap';
import { withTracker } from 'meteor/react-meteor-data';
import { Meteor } from 'meteor/meteor';
import { Bert } from 'meteor/themeteorchef:bert';
import Products from '../../../api/Products/Products';
import NotFound from '../NotFound/NotFound';
import Loading from '../../components/Loading/Loading';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import moment from 'moment';
import "moment/locale/fr";
import { FormattedNumber } from 'react-intl';
import currencyUtils from '../../../modules/currency-utils';

import './ViewProduct.scss';

const data = [
      {name: '10/12/2017', price: 4000, currency: 'EUR'},
      {name: '15/12/2017', price: 3000, currency: 'EUR'},
      {name: '27/12/2017', price: 2000, currency: 'EUR'},
      {name: '10/01/2018', price: 2780, currency: 'EUR'},
      {name: '14/01/2018', price: 1890, currency: 'EUR'},
      {name: '25/01/2018', price: 2390, currency: 'EUR'},
      {name: '27/01/2018', price: 699, currency: 'EUR'},
];

class CustomTooltip extends React.Component {
  propTypes: {
    type: PropTypes.string,
    payload: PropTypes.array,
    label: PropTypes.string,
  }

  render() {
    const { active } = this.props;

    if (active) {
      const { payload, label } = this.props;
      return (
        <div className="rechart-custom-tooltip">
          <span>{moment(payload[0].payload.name, "DD/MM/YYYY").format('LL')}</span>
          <span><FormattedNumber value={payload[0].payload.price} style="currency" currency={payload[0].payload.currency} /></span>
        </div>
      );
    }

    return null;
  }
}



const ViewProduct = ({ loading, product, match, history }) =>
  !loading ? (
    <div>
    <div id="product">
      <div id="product-img">
        <img
          src={'/img/products/' + product.image_name + '.jpg'}
          alt={product.name}
        />
      </div>
      <div id="product-info">
        <div className="product-name">
          <h1>{product.name}</h1>
        </div>
        <div className="product-price">
          <FormattedNumber value={product.price} style="currency" currency={product.currency} />
        </div>
        <div className="product-avis">
          {!product.nb_avis ? (<span>Aucun avis</span>) : (<span>{product.rate}/{product.max_rate} ({product.nb_avis} avis)</span>)}
        </div>
      </div>
      <div id="product-price-chart">
      <ResponsiveContainer>
        <LineChart data={data}>
          <Line dataKey="price" stroke="#FF6600" activeDot={{r: 6}}/>
          <CartesianGrid stroke="#ccc" strokeDasharray="3 3" />
          <XAxis tick={false} stroke="#ccc" />
          <YAxis stroke="#ccc" domain={['auto', 'auto']}/>
          <Tooltip content={<CustomTooltip />}/>
        </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
    <div id="stores">
      <h2>Disponible sur :</h2>
      <ul>
        <li>
            <div className="store-logo">
              <img
                src={'/img/stores/logos/' + product.store + '.png'}
                alt={product.store}
              />
            </div>
            <div className="store-product-avis">{!product.nb_avis ? (<span>Aucun avis</span>) : (<span>{product.rate}/{product.max_rate} ({product.nb_avis} avis)</span>)}</div>
            <div className="store-product-name"><h3>{product.name}</h3></div>
            <div className="store-product-price"><span className="price"><FormattedNumber value={product.price} style="currency" currency={product.currency} /></span></div>
            <div className="store-product-link"><a href={product.url} target="_blank">Voir l'offre</a></div>
        </li>
      </ul>
    </div>
    </div>
  ) : (
    <Loading />
  );

ViewProduct.propTypes = {
  loading: PropTypes.bool.isRequired,
  product: PropTypes.object,
  match: PropTypes.object.isRequired,
  history: PropTypes.object.isRequired,
};

export default withTracker(({ match }) => {
  const productId = match.params._id;
  const subscription = Meteor.subscribe('products.view', productId);
console.log(Products.findOne(new Mongo.ObjectID(productId)))
  return {
    loading: !subscription.ready(),
    product: Products.findOne(new Mongo.ObjectID(productId)),
  };
})(ViewProduct);
