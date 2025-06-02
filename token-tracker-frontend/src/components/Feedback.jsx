import React from 'react';

function Feedback({ traceId }) {
  const [rating, setRating] = React.useState(null);
  const [comments, setComments] = React.useState('');

  async function handleSubmit() {
    if (rating !== null) {
      const feedbackData = { rating, comments, traceId };
      try {
        const response = await fetch('http://localhost:8000/api/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(feedbackData),
        });
        if (!response.ok) throw new Error('Failed to send feedback');
        alert('Feedback submitted, thanks!');
      } catch (e) {
        alert('Error submitting feedback');
      }

      // Clear form inputs after submission
      setRating(null);
      setComments('');
    } else {
      alert('Please provide a rating');
    }
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <h4>Feedback</h4>
      <div style={{ marginBottom: '10px' }}>
        <button
        onClick={() => setRating('👍')}
        style={{ marginRight: '1rem', padding: '0.5rem 1rem' }}
        >
        👍
        </button>
        <button
        onClick={() => setRating('👎')}
        style={{ padding: '0.5rem 1rem' }}
        >
        👎
        </button>
      </div>
        <textarea
        placeholder="Additional comments"
        rows="4"
        cols="50"
        style={{ display: 'block', width: '100%', margin: '1rem 0', padding: '0.5rem' }}
        value={comments}
        onChange={(e) => setComments(e.target.value)}
        />
      <br />
      <button onClick={handleSubmit}>Submit Feedback</button>
    </div>
  );
}

export default Feedback;
