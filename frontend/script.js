const apiUrl = 'http://localhost:8000';
const app = document.getElementById('app-root');

const routes = {
    '#home': renderHome,
    '#login': renderLogin,
    '#register': renderRegister,
    '#dashboard': renderDashboard,
    '#poc': renderPocDetails
};

function router() {
    updateNavLinks();
    const path = window.location.hash || '#home';
    const renderer = routes[path.split('/')[0]];
    if (renderer) {
        renderer();
    } else {
        app.innerHTML = '<h1>404 Not Found</h1>';
    }
}

window.addEventListener('hashchange', router);
window.addEventListener('load', router);

async function renderHome() {
    try {
        const response = await fetch(`${apiUrl}/pocs`);
        const pocs = await response.json();
        app.innerHTML = `
            <h1>Available POCs</h1>
            ${pocs.map(poc => `
                <div class="card">
                    <h2>${poc.title}</h2>
                    <p>${poc.description}</p>
                    <a href="#poc/${poc.id}">View Details</a>
                </div>
            `).join('')}
        `;
    } catch (error) {
        console.error('Failed to fetch POCs', error);
                app.innerHTML = '<h1>Error loading POCs</h1>';
    }
}

function renderLogin() {
    app.innerHTML = `
        <h1>Login</h1>
        <form id="login-form">
            <input type="email" id="email" placeholder="Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    `;
    const form = document.getElementById('login-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch(`${apiUrl}/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ username: email, password })
            });
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                window.location.hash = '#dashboard';
            } else {
                alert('Login failed');
            }
        } catch (error) {
            console.error('Login error', error);
        }
    });
}

function renderRegister() {
    app.innerHTML = `
        <h1>Register</h1>
        <form id="register-form">
            <input type="text" id="fullName" placeholder="Full Name" required>
            <input type="email" id="email" placeholder="Email" required>
            <input type="text" id="designation" placeholder="Designation" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
    `;
    const form = document.getElementById('register-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const designation = document.getElementById('designation').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch(`${apiUrl}/users`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_name: fullName, email, designation, password })
            });
            if (response.ok) {
                window.location.hash = '#login';
            } else {
                alert('Registration failed');
            }
        } catch (error) {
            console.error('Registration error', error);
        }
    });
}