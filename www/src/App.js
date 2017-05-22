// @flow

import type {TenureType} from './types';

import React, { Component } from 'react';
import logo from './logo.svg';
import Tenure from './Tenure';
import './App.css';

type State = {
  tenureData: ?TenureType,
};

export default class App extends Component<void, void, State> {
  state = {
    tenureData: null,
  };

  componentDidMount() {
    fetch('./tenure.json')
      .then((response) => response.json())
      .then((tenureData) => {
        this.setState({
          tenureData: tenureData,
        });
      });
  }

  render() {
    if (this.state.tenureData) {
      return (
        <Tenure data={this.state.tenureData} />
      );
    }

    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Loading</h2>
        </div>
      </div>
    );
  }
}
