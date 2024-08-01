import React, { Component } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Table from 'react-bootstrap/Table'
import SearchRow from './SearchRow';

class SearchHistory extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searches: []
    };
  };

  componentDidMount() {
    this.fetchSearches();
    this.timerID = setInterval(
      () => this.fetchSearches(),
      1000
    );
  };

  componentWillUnmount() {
    clearInterval(this.timerID);
  };

  fetchSearches() {
    fetch('/searches/')
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: 'Something went wrong!' };
          });
        };
        return response.json();
      })
      .then(searches => {
        this.setState(() => {
          return {
            searches
          };
        });
      });
  };

  getTableHeader() {
    return (
      <thead>
        <tr>
	  <th>Status</th>
	  <th>Runtime</th>
          <th>Sequence</th>
          <th>Genome</th>
          <th>Protein</th>
	  <th>Start</th>
	  <th>End</th>
        </tr>
      </thead>
    );
  };

  render() {
    const search_rows = this.state.searches.map(search => {
      return (
        <SearchRow search={search}/>
      );
    });

    if (search_rows.length > 0) {
      return (
        <Row className='search-history justify-content-md-center'>
	  <Col md={9}>
	    <Row className='search-history-header'>
              <p>Search History</p>
	    </Row>
            <Table responsive bordered hover>
	      {this.getTableHeader()}
	      <tbody>
	        {search_rows}
	      </tbody>
	    </Table>
	  </Col>
        </Row>
      );
    };
  };
};

export default SearchHistory;

