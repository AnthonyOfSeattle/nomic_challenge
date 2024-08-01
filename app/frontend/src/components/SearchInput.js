import React, { Component } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

class SearchInput extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.state = {
      sequence: ''
    };
  };

  isSequenceValid() {
    const validator = new RegExp('[^ATCG]');
    return !validator.test(this.state.sequence);
  };

  handleChange(e) {
    if (this.props.maxInputLength != null) {
      this.setState({
        sequence: e.target.value.slice(0, this.props.maxInputLength)
      });
    } else {
      this.setState({
        sequence: e.target.value
      });
    };
  };

  handleSubmit(e) {
    if (this.state.sequence.length > 0 &&
          this.isSequenceValid()) {
      this.postSearch();
      this.setState({ sequence: '' });
    };
    e.preventDefault();
  };

  postSearch() {
    fetch('/searches/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'}, 
      body: JSON.stringify(this.state)
    });
  };

  render() {
    return (
      <Row className='search-input justify-content-md-center'>
	<Col md={9} className='search-input-card'>
          <Form onSubmit={this.handleSubmit} className='search-input-form'>
            <Form.Group
              className='mb-2'
              controlId='formBasicText'
            >
              <Form.Label>Sequence Search</Form.Label>
              <Form.Control 
                type='text' 
                placeholder='Enter DNA sequence' 
                value={this.state.sequence}
                onChange={this.handleChange}
	        className={this.isSequenceValid() ? 
			     '.form-control-valid' : 
			     'form-control-invalid'}
              />
            </Form.Group>
            <Button variant='primary' type='submit'>
              Submit
            </Button>
          </Form>
	</Col>
      </Row>
    );
  };
};

export default SearchInput;
