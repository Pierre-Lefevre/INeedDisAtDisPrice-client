import React from 'react';
import { render } from 'react-dom';
import { createStore } from 'redux'
import { Provider } from 'react-redux'
import App from './App.jsx';
import todoApp from '../redux/reducers/reducers.js'

let store = createStore(todoApp)

render(
  <Provider store = {store}>
    <App />
  </Provider>, document.getElementById('app')
);