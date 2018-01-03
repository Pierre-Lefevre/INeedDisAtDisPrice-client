import React from 'react'
import PropTypes from 'prop-types'
import { Component } from 'react'
import { Link } from 'react-router';

export default class ProductItem extends Component {
  constructor (props) {
    super(props)
  }

  render () {
    const {product} = this.props
console.log(product)
    return (
      <div>
        <Link
          to={`/product/${product._id}`}
          key={product._id}
          title={product.name}
        >
          <img src={"img/products/" + product.image_name + ".jpg"}/>
          {product.name}
        </Link>
      </div>
    )
  }
}

ProductItem.propTypes = {
  product: PropTypes.object,
}