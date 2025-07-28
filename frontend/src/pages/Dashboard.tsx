import { useState, useEffect } from 'react';
import api from '../services/api';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const Dashboard = () => {
  const [myPocs, setMyPocs] = useState([]);
  const [myApplications, setMyApplications] = useState([]);

  useEffect(() => {
    // This is a simplified implementation. 
    // In a real app, you'd have dedicated endpoints to get this data.
    api.get('/users/me').then(userResponse => {
      const userId = userResponse.data.id;
      api.get('/pocs').then(pocsResponse => {
        setMyPocs(pocsResponse.data.filter(poc => poc.owner.id === userId));
      });
      api.get('/applications').then(appsResponse => {
        setMyApplications(appsResponse.data.filter(app => app.applicant.id === userId));
      });
    });
  }, []);

  return (
    <Container>
      <h1>Dashboard</h1>
      <Row>
        <Col md={6}>
          <h2>My Posted POCs</h2>
          {myPocs.map(poc => (
            <Card key={poc.id} className="mb-3">
              <Card.Body>
                <Card.Title>{poc.title}</Card.Title>
                {/* Further details and application management would go here */}
              </Card.Body>
            </Card>
          ))}
        </Col>
        <Col md={6}>
          <h2>My Applications</h2>
          {myApplications.map(app => (
            <Card key={app.id} className="mb-3">
              <Card.Body>
                <Card.Title>{/* POC Title would be fetched here */}</Card.Title>
                <Card.Text>Status: {app.status}</Card.Text>
              </Card.Body>
            </Card>
          ))}
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
