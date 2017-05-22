// @flow

import React, { Component } from 'react';
import * as d3 from "d3";

type Props = {
  width?: number,
  height?: number,
  data: any,
};

export default class SVG extends Component<void, Props, void> {
  componentDidMount() {
    this.renderGraph();
  }

  componentDidUpdate() {
    this.renderGraph();
  }

  renderGraph() {
    const data = this.props.data;
    const svg = d3.select("svg");

    const dateParser = d3.timeParse('%Y-%m-%d');

    const margin = {
      top: 20,
      right: 20,
      bottom: 30,
      left: 40,
    };
    const width = Number(svg.attr("width")) - margin.left - margin.right;
    const height = Number(svg.attr("height")) - margin.top - margin.bottom;

    const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
    const y = d3.scaleLinear().rangeRound([height, 0]);

    const g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x.domain(
      data.map((d, index) => {
        return dateParser(d.date);
      })
    );
    y.domain([
      0, d3.max(data, (d) => d.count),
    ]);

    g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y).ticks(10))
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("Employee Count");

    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", (d) => x(dateParser(d.date)))
        .attr("y", (d) => y(d.count))
        .attr("width", x.bandwidth())
        .attr("height", function(d) { return height - y(d.count); });
  }

  render() {
    return <svg width={this.props.width || 960} height={this.props.height || 500}></svg>;
  }
}
