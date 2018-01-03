import React from 'react'
import axios from 'axios'

export default class Product extends React.Component {
  constructor (props) {
    super(props)
    this.state = {product: null}
  }

  componentWillMount () {
    this.getData(this)
  }

  getData (ev) {
    axios.get('/getOne').then(function (response) {
      console.log(response.data)
      ev.setState({product: response.data})
    })
  }

  render () {
    return (<div>{this.state.product != null ? this.state.product.name : ''}</div>)
  }
}
