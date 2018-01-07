import React from 'react'
import logo from './logo.svg'
import axios from 'axios'
import { codeToSymbol } from './currency-utils'
import { Link } from 'react-router-dom'

import './ProductsList.css'

export default class ProductsList extends React.Component {
  constructor (props) {
    super(props)

    this.state = {products: []}
  }

  componentDidMount () {
    this.ProductsList()
  }

  ProductsList () {
    axios.get('http://127.0.0.1:3333/api/products')
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
            <img src={logo} className="App-logo" alt="logo"/>
            <h1 className="App-title">Welcome to React</h1>
          </header>
          <p className="App-intro">
            To get started, edit <code>src/App.js</code> and save to reload.
          </p>
        </div>
        <ul id="products-list">{persons}</ul>
      </div>
    )
  }
}
