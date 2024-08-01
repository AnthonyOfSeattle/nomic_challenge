import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import SearchHistory from './SearchHistory';
import SearchInput from './SearchInput';

class SearchApp extends Component {
  render() {
    return (
      <Container className='search-app'>
	<SearchInput maxInputLength={this.props.maxInputLength} />
        <SearchHistory />
      </Container>
    );
  };
};

export default SearchApp;
