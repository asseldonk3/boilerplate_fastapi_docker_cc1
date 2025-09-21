// Vanilla JavaScript - no build tools, no transpilation!

const API_BASE = 'http://localhost:8001';

// Check system status on load
window.addEventListener('DOMContentLoaded', checkStatus);

async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/`);
        const data = await response.json();
        document.getElementById('status').innerHTML = `
            <span class="status-ok">✓ Connected</span> |
            Project: ${data.project} |
            Server Time: ${new Date(data.timestamp).toLocaleTimeString()}
        `;
    } catch (error) {
        document.getElementById('status').innerHTML =
            '<span class="status-error">✗ Cannot connect to backend</span>';
    }
}

async function testAPI() {
    const prompt = document.getElementById('promptInput').value;
    const resultDiv = document.getElementById('result');

    if (!prompt) {
        alert('Please enter a prompt');
        return;
    }

    resultDiv.textContent = 'Thinking...';
    resultDiv.classList.add('show');

    try {
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();
        resultDiv.textContent = data.response || 'No response';
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    }
}

// Auto-refresh status every 30 seconds
setInterval(checkStatus, 30000);
