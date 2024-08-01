import React, { Component } from 'react';

class SearchRow extends Component {
  getFullStatus() {
    const status_codes = {S : 'SUBMITTED',
                          R : 'RUNNING',
                          C : 'COMPLETE',
                          E : 'ERROR'};

    return status_codes[this.props.search.status];
  };

  getStatusClass() {
    const status_classes = {S : 'table-secondary',
                            R : 'table-primary',
                            C : 'table-success',
                            E : 'table-danger'};

    return status_classes[this.props.search.status];
  }

  getSearchRuntime() {
    const started = new Date(this.props.search.started);
    var finished = new Date(Date.now());
    if (this.getFullStatus() == 'COMPLETE' ||
          this.getFullStatus() == 'ERROR') {
      finished = new Date(this.props.search.finished);
    };

    const runtime = (finished - started)/1000;

    return runtime.toFixed(2);

  }

  renderSearchResults() {
    if (this.getFullStatus() != 'COMPLETE') {
      return (
        [...Array(4)].map(() => {<td></td>})
      );
    };

    const result = this.props.search.results[0];
    return (
      [<td>{result.genome}</td>,
       <td>{result.protein}</td>,
       <td>{result.start}</td>,
       <td>{result.end}</td>]
    );
  };

  render() {
    return (
      <tr>
	<td class={this.getStatusClass()}>{this.getFullStatus()}</td>
	<td>{this.getSearchRuntime()}</td>
        <td>{this.props.search.sequence}</td>
	{this.renderSearchResults()}
      </tr>
    );
  };
};

export default SearchRow;

