import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Container, Card, Button } from 'react-bootstrap';

const Home = () => {
  const [pocs, setPocs] = useState([]);

  useEffect(() => {
    api.get('/pocs').then(response => {
      setPocs(response.data);
    });
  }, []);

  return (
    <Container>
      <h1>Available POCs</h1>
      {pocs.map(poc => (
        <Card key={poc.id} className="mb-3">
          <Card.Body>
            <Card.Title>{poc.title}</Card.Title>
            <Card.Text>{poc.description}</Card.Text>
            <Link to={`/poc/${poc.id}`}>
              <Button variant="primary">View Details</Button>
            </Link>
          </Card.Body>
        </Card>
      ))}
    </Container>
  );
};

export default Home;
