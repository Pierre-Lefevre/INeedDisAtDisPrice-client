import React from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import moment from 'moment'
import 'moment/locale/fr'
import { FormattedNumber } from 'react-intl'
import Loader from '../../components/Loader/Loader'

import './Product.css'

const data = [
  {name: '10/12/2017', price: 4000, currency: 'EUR'},
  {name: '15/12/2017', price: 3000, currency: 'EUR'},
  {name: '27/12/2017', price: 2000, currency: 'EUR'},
  {name: '10/01/2018', price: 2780, currency: 'EUR'},
  {name: '14/01/2018', price: 1890, currency: 'EUR'},
  {name: '25/01/2018', price: 2390, currency: 'EUR'},
  {name: '27/01/2018', price: 699, currency: 'EUR'},
]

class CustomTooltip extends React.Component {
  render () {
    const {active} = this.props
    if (active) {
      const {payload} = this.props
      return (
        <div className="rechart-custom-tooltip">
          <span>{moment(payload[0].payload.name, 'DD/MM/YYYY').format('LL')}</span>
          <span><FormattedNumber value={payload[0].payload.price} style="currency" currency={payload[0].payload.currency}/></span>
        </div>
      )
    }
    return null
  }
}

export default class Product extends React.Component {
  constructor (props) {
    super(props)
    this.state = {product: null}
  }

  componentDidMount () {
    this.Product()
  }

  Product () {
    axios.get('http://localhost:4242/api/product/' + this.props.match.params.id)
      .then(res => {
        this.setState({product: res.data})
      })
  }

  render () {
    if (this.state.product) {
      let product = this.state.product
      return (
        <main>
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
              <div className="product-price price">
                <FormattedNumber value={product.price} style="currency" currency={product.currency}/>
              </div>
              <div className="product-avis">
                {!product.nb_avis ? (<span>Aucun avis</span>) : (<span>{product.rate}/{product.max_rate} ({product.nb_avis} avis)</span>)}
              </div>
            </div>
            <div id="product-price-chart">
              <ResponsiveContainer>
                <LineChart data={data}>
                  <Line dataKey="price" stroke="#FF6600" activeDot={{r: 6}}/>
                  <CartesianGrid stroke="#ccc" strokeDasharray="3 3"/>
                  <XAxis tick={false} stroke="#ccc"/>
                  <YAxis stroke="#ccc" domain={['auto', 'auto']}/>
                  <Tooltip content={<CustomTooltip/>}/>
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
                <div className="store-product-price price"><FormattedNumber value={product.price} style="currency" currency={product.currency}/></div>
                <div className="store-product-link"><a href={product.url} target="_blank">Voir l'offre</a></div>
              </li>
            </ul>
          </div>
        </main>)
    }
    return (<Loader/>)
  }
}
