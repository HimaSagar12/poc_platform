const apiUrl = 'http://localhost:8000';
const app = document.getElementById('app-root');

const routes = {
    '#home': renderHome,
    '#login': renderLogin,
    '#register': renderRegister,
    '#dashboard': renderDashboard,
    '#poc': renderPocDetails,
    '#create-poc': renderCreatePoc
};

function router() {
    // Proactively clear invalid tokens to ensure correct nav link display
    const currentToken = localStorage.getItem('token');
    if (currentToken && currentToken.split('.').length !== 3) { // Simple check for JWT format
        localStorage.removeItem('token');
    }
    updateNavLinks();
    const path = window.location.hash || '#home';
    console.log('Router: Current hash path:', path);
    const renderer = routes[path.split('/')[0]];
    console.log('Router: Renderer function:', renderer);
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
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const pocs = await response.json();

        if (Array.isArray(pocs)) {
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
        } else {
            console.error('API did not return an array of POCs', pocs);
            app.innerHTML = '<h1>Error: Invalid data received from server</h1>';
        }
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

async function renderDashboard() {
    console.log('renderDashboard called.');
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.hash = '#login';
        return;
    }

    updateNavLinks();

    try {
        const userResponse = await fetch(`${apiUrl}/users/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!userResponse.ok) throw new Error('Failed to fetch user');
        const user = await userResponse.json();
        const userId = user.id;

        const pocsResponse = await fetch(`${apiUrl}/pocs`);
        if (!pocsResponse.ok) throw new Error('Failed to fetch POCs');
        const allPocs = await pocsResponse.json();
        const myPocs = allPocs.filter(poc => poc.owner.id === userId);

        let myApplications = [];
        for (const poc of myPocs) {
            const appsResponse = await fetch(`${apiUrl}/applications/poc/${poc.id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (appsResponse.ok) {
                const apps = await appsResponse.json();
                myApplications.push(...apps);
            }
        }


        const dashboardHtml = `
            <h1>Dashboard</h1>
            <button onclick="window.location.hash = '#create-poc'" style="display: block; margin-bottom: 1rem; padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Create New POC</button>
            <div class="row">
                <div class="col">
                    <h2>My Posted POCs</h2>
                    <div id="my-pocs">
                        ${myPocs.length ? myPocs.map(poc => `
                            <div class="card">
                                <h3>${poc.title}</h3>
                            </div>
                        `).join('') : '<p>You have not posted any POCs.</p>'}
                    </div>
                </div>
                <div class="col">
                    <h2>My Applications</h2>
                     <div id="my-applications">
                        ${myApplications.length ? myApplications.map(app => `
                            <div class="card">
                                <p>Status: ${app.status}</p>
                            </div>
                        `).join('') : '<p>You have not applied to any POCs.</p>'}
                    </div>
                </div>
            </div>
        `;
        console.log("Generated Dashboard HTML:", dashboardHtml);
        app.innerHTML = dashboardHtml;
    } catch (error) {
        console.error('Failed to load dashboard', error);
        app.innerHTML = '<h1>Error loading dashboard</h1>';
        localStorage.removeItem('token'); // Clear bad token
        window.location.hash = '#login';
    }
}

async function renderPocDetails() {
    const pocId = window.location.hash.split('/')[1];
    if (!pocId) {
        app.innerHTML = '<h1>Invalid POC ID</h1>';
        return;
    }

    try {
        const pocResponse = await fetch(`${apiUrl}/pocs/${pocId}`);
        if (!pocResponse.ok) throw new Error('Failed to fetch POC details');
        const poc = await pocResponse.json();

        const commentsResponse = await fetch(`${apiUrl}/comments/poc/${pocId}`);
        if (!commentsResponse.ok) throw new Error('Failed to fetch comments');
        const comments = await commentsResponse.json();

        app.innerHTML = `
            <div class="card">
                <h1>${poc.title}</h1>
                <p>${poc.description}</p>
                <p>Posted by: ${poc.owner.full_name} (${poc.owner.designation})</p>
            </div>

            <div class="mt-4">
                <h3>Comments</h3>
                <div id="comments-section">
                    ${comments.length ? comments.map(comment => `
                        <div><strong>${comment.author.full_name}:</strong> ${comment.text}</div>
                    `).join('') : '<p>No comments yet.</p>'}
                </div>
                <form id="comment-form">
                    <textarea id="new-comment" placeholder="Write a comment..." rows="3" required></textarea>
                    <button type="submit">Post Comment</button>
                </form>
            </div>
        `;

        const commentForm = document.getElementById('comment-form');
        commentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const newCommentText = document.getElementById('new-comment').value;
            const token = localStorage.getItem('token');
            if (!token) {
                alert('You must be logged in to comment.');
                window.location.hash = '#login';
                return;
            }

            try {
                const response = await fetch(`${apiUrl}/comments`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: newCommentText, poc_id: parseInt(pocId) })
                });

                if (response.ok) {
                    renderPocDetails(); // Re-render to show the new comment
                } else {
                    const errorData = await response.json();
                    alert(`Failed to post comment: ${errorData.detail || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Failed to post comment', error);
            }
        });

    } catch (error) {
        console.error('Failed to load POC details', error);
        app.innerHTML = '<h1>Error loading POC details</h1>';
    }
}

async function renderCreatePoc() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.hash = '#login';
        return;
    }

    app.innerHTML = `
        <h1>Create New POC</h1>
        <form id="create-poc-form">
            <label for="poc-title">Title:</label>
            <input type="text" id="poc-title" required>
            <label for="poc-description">Description:</label>
            <textarea id="poc-description" rows="5" required></textarea>
            <button type="submit">Create POC</button>
        </form>
    `;

    const form = document.getElementById('create-poc-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('poc-title').value;
        const description = document.getElementById('poc-description').value;

        try {
            const response = await fetch(`${apiUrl}/pocs`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title, description })
            });

            if (response.ok) {
                alert('POC created successfully!');
                window.location.hash = '#dashboard';
            } else {
                const errorData = await response.json();
                alert(`Failed to create POC: ${errorData.detail || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error creating POC', error);
            alert('An error occurred while creating the POC.');
        }
    });
}

function updateNavLinks() {
    const token = localStorage.getItem('token');
    const loginLink = document.getElementById('login-link');
    const registerLink = document.getElementById('register-link');
    const dashboardLink = document.getElementById('dashboard-link');

    console.log('updateNavLinks called. Token:', token);

    if (token) {
        loginLink.style.display = 'none';
        registerLink.style.display = 'none';
        dashboardLink.style.display = 'block';
    } else {
        loginLink.style.display = 'block';
        registerLink.style.display = 'block';
        dashboardLink.style.display = 'none';
    }
}