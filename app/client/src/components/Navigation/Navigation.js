import React from 'react'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom'

import './Navigation.css'

export default class Navigation extends React.Component {

  login () {
    this.props.auth.login()
  }

  logout () {
    this.props.auth.logout()
  }

  render () {
    const {isAuthenticated} = this.props.auth
    return (
      <nav>
        <div id="brand">
          <Link to="/">I Need Dis At Dis Price</Link>
        </div>
        <div id="menu-container">
          <ul className="menu">
            <li><Link to="/products">Produits</Link></li>
          </ul>
          {isAuthenticated() ? <ul className="menu authenticated-navigation">
              <li><Link to="/profile">Profil</Link></li>
              <li><a onClick={this.logout.bind(this)}>Déconnexion</a></li>
            </ul>
            : <ul className="menu authenticated-navigation">
              <li><a onClick={this.login.bind(this)}>Connexion</a></li>
            </ul>
          }
        </div>
      </nav>
    )
  }
}

Navigation.propTypes = {
  auth: PropTypes.object.isRequired,
}
