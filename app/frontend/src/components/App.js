import React, { Component } from 'react';
import { render } from 'react-dom';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import SearchApp from './SearchApp';

function Banner() {
  return (
    <Navbar variant='light'>
      <Container>
        <Navbar.Brand>Seqsleuth</Navbar.Brand>
      </Container>
    </Navbar>
  );
};

class App extends Component {
  render() {
    return (
      <Container>
	<Banner />
	<SearchApp maxInputLength={200} />
      </Container>
    );
  };
};

export default App;

const container = document.getElementById('app');
render(<App />, container);
