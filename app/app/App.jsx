import React, { Component } from 'react'
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom'
import Home from './Home.js'
import Login from './Login.js'

import { connect } from 'react-redux'
import { addTodo } from '../redux/actions/actions.js'

import AddTodo from '../components/AddTodo.js'
import TodoList from '../components/TodoList.js'

class App extends Component {
  render () {
    const { dispatch, visibleTodos } = this.props

    return (
      <Router>
        <div>
          <div>
            <AddTodo onAddClick = {text => dispatch(addTodo(text))} />
            <TodoList todos = {visibleTodos}/>
          </div>
          <h2>Welcome to React Router Tutorial</h2>
          <ul>
            <li><Link to={'/'}>Home</Link></li>
            <li><Link to={'/Login'}>Login</Link></li>
          </ul>
          <hr/>

          <Switch>
            <Route exact path='/' component={Home}/>
            <Route exact path='/Login' component={Login}/>
          </Switch>
        </div>
      </Router>
    )
  }
}
function select(state) {
  return {
    visibleTodos: state.todos
  }
}
export default connect(select)(App);