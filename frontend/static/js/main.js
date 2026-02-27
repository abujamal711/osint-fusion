let token = localStorage.getItem('token');
let username = localStorage.getItem('username');

function setAuth(token, user) {
    localStorage.setItem('token', token);
    localStorage.setItem('username', user);
    window.location.href = '/dashboard';
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

document.addEventListener('DOMContentLoaded', function() {
    // Login form handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            });
            const data = await response.json();
            if (response.ok) {
                setAuth(data.token, data.username);
            } else {
                alert(data.message);
            }
        });
    }

    // Register form handler
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('regUsername').value;
            const password = document.getElementById('regPassword').value;
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            });
            const data = await response.json();
            alert(data.message);
            if (response.ok) window.location.href = '/login';
        });
    }

    // Dashboard search
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        loadHistory();
        searchForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const target = document.getElementById('target').value;
            const type = document.getElementById('type').value;
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({target, type})
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('result').textContent = JSON.stringify(data.result, null, 2);
                loadHistory();
            } else {
                alert(data.message);
            }
        });
    }

    async function loadHistory() {
        const response = await fetch('/api/history', {
            headers: {'Authorization': 'Bearer ' + token}
        });
        const data = await response.json();
        const historyDiv = document.getElementById('history');
        if (historyDiv) {
            historyDiv.innerHTML = data.map(s => `
                <div class="card">
                    <strong>${s.target}</strong> (${s.type}) - ${new Date(s.timestamp).toLocaleString()}
                    <pre>${JSON.stringify(s.result, null, 2)}</pre>
                </div>
            `).join('');
        }
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) logoutBtn.addEventListener('click', logout);
});
