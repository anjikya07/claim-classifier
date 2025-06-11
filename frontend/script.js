async function classifyClaim() {
  const data = {
    claim_text: document.getElementById('claim').value,
    claimant_history: {
      claims_count: Number(document.getElementById('claimsCount').value),
      previous_denials: Number(document.getElementById('denials').value),
      profile_score: Number(document.getElementById('score').value)
    }
  };

  const resultBox = document.getElementById("result");
  resultBox.innerText = "Processing...";

  try {
    const response = await fetch('https://your-backend-api.com/api/classify-claim', {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const res = await response.json();
    resultBox.innerText = `Prediction: ${res.result} (Confidence: ${res.confidence})`;
  } catch (err) {
    resultBox.innerText = "Error contacting the server.";
  }
}