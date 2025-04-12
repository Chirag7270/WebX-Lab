function predictPersonality() {
  const text = document.getElementById('input-text').value;

  if (!text.trim()) {
    alert('Please enter some text!');
    return;
  }

  fetch('/api/predict', {
    method: 'POST',
    body: JSON.stringify({ text }),
    headers: { 'Content-Type': 'application/json' }
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert(data.error);
    } else {
      document.getElementById('result-text').innerText = `Predicted Personality: ${data.personality_type}`;
      document.getElementById('quote-text').innerText = `"${data.quote}"`;
      document.getElementById('results').style.display = 'block';
    }
  })
  .catch(error => console.error('Error:', error));
}
