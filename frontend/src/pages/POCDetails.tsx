import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { Container, Card, Form, Button } from 'react-bootstrap';

const POCDetails = () => {
  const { id } = useParams();
  const [poc, setPoc] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');

  useEffect(() => {
    api.get(`/pocs/${id}`).then(response => setPoc(response.data));
    api.get(`/comments/poc/${id}`).then(response => setComments(response.data));
  }, [id]);

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/comments', { text: newComment, poc_id: id });
      setComments([...comments, response.data]);
      setNewComment('');
    } catch (error) {
      console.error('Failed to post comment', error);
    }
  };

  if (!poc) return <div>Loading...</div>;

  return (
    <Container>
      <Card>
        <Card.Body>
          <Card.Title>{poc.title}</Card.Title>
          <Card.Text>{poc.description}</Card.Text>
          <p>Posted by: {poc.owner.full_name} ({poc.owner.designation})</p>
        </Card.Body>
      </Card>

      <div className="mt-4">
        <h3>Comments</h3>
        {comments.map(comment => (
          <div key={comment.id} className="mb-2">
            <strong>{comment.author.full_name}:</strong> {comment.text}
          </div>
        ))}
        <Form onSubmit={handleCommentSubmit}>
          <Form.Group className="mb-3">
            <Form.Control 
              as="textarea" 
              rows={3} 
              value={newComment} 
              onChange={(e) => setNewComment(e.target.value)}
            />
          </Form.Group>
          <Button type="submit">Post Comment</Button>
        </Form>
      </div>
    </Container>
  );
};

export default POCDetails;
