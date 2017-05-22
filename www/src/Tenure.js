// @flow

import type {TenureType} from './types';

import React, { Component } from 'react';
import SVG from './SVG';

type Props = {
  data: TenureType,
};

export default class Tenure extends Component<void, Props, void> {
  render() {

    const data = Object.keys(this.props.data)
      .map((key) => this.props.data[key])
      .map((item, index, items) => ({
        date: item.date,
        count: item.count,
      }));

    return <SVG data={data} />;
  }
}
