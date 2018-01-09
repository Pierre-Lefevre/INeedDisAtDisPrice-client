import React from 'react'
import axios from 'axios'
import { codeToSymbol } from '../../modules/currency-utils'
import { Link } from 'react-router-dom'
import Loader from '../../components/Loader/Loader'

import './Products.css'

export default class Products extends React.Component {
  constructor (props) {
    super(props)

    this.state = {products: []}
  }

  componentDidMount () {
    this.ProductsList()
  }

  ProductsList () {
    axios.get('http://localhost:4242/api/products')
      .then(res => {
        this.setState({products: res.data})
      })
  }

  render () {
    if (this.state.products.length !== 0) {
      const persons = this.state.products.map((item, i) => (
        <li key={item._id}>
          <Link to={this.props.match.url + '' + item._id}>
            <figure>
              <img src={'/img/products/' + item.image_name + '.jpg'} alt={item.name}/>
              <figcaption>
                <div className="product-name">{item.name}</div>
                <div className="product-price price">
                  {item.price.toFixed(2)} {codeToSymbol(item.currency)}
                </div>
              </figcaption>
            </figure>
          </Link>
        </li>
      ))
      return (
        <main>
          <ul id="products-list">{persons}</ul>
        </main>
      )
    }
    return (<Loader/>)
  }
}
