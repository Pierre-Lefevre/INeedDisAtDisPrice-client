import React from 'react'
import axios from 'axios'
import { codeToSymbol } from '../../modules/currency-utils'
import { Link } from 'react-router-dom'

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
    console.log(this.state.products)
    const persons = this.state.products.map((item, i) => (
      <li key={item._id}>
        <Link to={this.props.match.url + '' + item._id}>
          <figure>
            <img src={'/img/products/' + item.image_name + '.jpg'} alt={item.name}/>
            <figcaption>
              <div className="product-name">{item.name}</div>
              <div className="product-price">
                {item.price.toFixed(2)} {codeToSymbol(item.currency)}
              </div>
            </figcaption>
          </figure>
        </Link>
      </li>
    ))

    return (<div>
        <div className="App">
          <header className="App-header">
            <img src="/svg/logo.svg" className="App-logo" alt="logo"/>
            <h1 className="App-title">I Need Dis At Dis Price</h1>
          </header>
        </div>
        <ul id="products-list">{persons}</ul>
      </div>
    )
  }
}
