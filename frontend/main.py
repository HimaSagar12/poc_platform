import react
from browser import document, html, ajax, window, local_storage

class App(react.Component):
    def __init__(self):
        self.state = {
            'pocs': [],
            'my_pocs': [],
            'my_applications': [],
            'user': None,
            'route': window.location.hash,
            'token': local_storage.getItem('token'),
            'current_poc': None,
            'comments': []
        }

    def componentDidMount(self):
        window.bind('hashchange', self.on_hash_change)
        self.router()

    def on_hash_change(self, event):
        self.setState({'route': window.location.hash})
        self.router()

    def router(self):
        route = self.state['route']
        if self.state['token']:
            if route in ['#login', '#register']:
                self.setState({'route': '#dashboard'})
            else:
                self.setState({'route': route or '#dashboard'})
        else:
            self.setState({'route': route or '#home'})

        if route.startswith('#poc/'):
            poc_id = route.split('/')[1]
            self.fetch_poc_details(poc_id)
        elif route == '#home':
            ajax.get('/pocs', oncomplete=self.on_pocs_loaded)
        elif route == '#dashboard':
            self.fetch_dashboard_data()

    def fetch_poc_details(self, poc_id):
        ajax.get(f'/pocs/{poc_id}', oncomplete=self.on_poc_details_loaded)
        ajax.get(f'/comments/poc/{poc_id}', oncomplete=self.on_comments_loaded)

    def on_poc_details_loaded(self, req):
        if req.status == 200:
            self.setState({'current_poc': req.json})

    def on_comments_loaded(self, req):
        if req.status == 200:
            self.setState({'comments': req.json})

    def on_pocs_loaded(self, req):
        self.setState({'pocs': req.json})

    def fetch_dashboard_data(self):
        headers = {'Authorization': f'Bearer {self.state["token"]}'}
        ajax.get('/users/me', headers=headers, oncomplete=self.on_user_loaded)

    def on_user_loaded(self, req):
        if req.status == 200:
            self.setState({'user': req.json})
            ajax.get('/pocs', oncomplete=self.on_all_pocs_loaded)
        else:
            self.logout()

    def on_all_pocs_loaded(self, req):
        all_pocs = req.json
        my_pocs = [poc for poc in all_pocs if poc['owner']['id'] == self.state['user']['id']]
        self.setState({'my_pocs': my_pocs})
        for poc in my_pocs:
            headers = {'Authorization': f'Bearer {self.state["token"]}'}
            ajax.get(f'/applications/poc/{poc["id"]}', headers=headers, oncomplete=self.on_applications_loaded)

    def on_applications_loaded(self, req):
        if req.status == 200:
            self.setState({'my_applications': self.state['my_applications'] + req.json})

    def logout(self):
        local_storage.removeItem('token')
        self.setState({'token': None, 'route': '#login'})

    def render(self):
        nav = html.NAV([
            html.A('Home', href='#home'),
            html.A('Login', href='#login', style={'display': 'none' if self.state['token'] else 'block'}),
            html.A('Register', href='#register', style={'display': 'none' if self.state['token'] else 'block'}),
            html.A('Dashboard', href='#dashboard', style={'display': 'block' if self.state['token'] else 'none'})
        ])

        route = self.state['route']
        if route == '#home':
            content = html.DIV([
                html.H1('Available POCs'),
                html.DIV([ 
                    html.DIV([
                        html.H2(poc['title']),
                        html.P(poc['description']),
                        html.A('View Details', href=f'#poc/{poc["id"]}')
                    ], className='card') for poc in self.state['pocs']
                ])
            ])
        elif route == '#login':
            content = html.DIV([
                html.H1('Login'),
                html.FORM([
                    html.INPUT(type='email', placeholder='Email', id='email'),
                    html.INPUT(type='password', placeholder='Password', id='password'),
                    html.BUTTON('Login', type='submit')
                ], onSubmit=self.handle_login)
            ])
        elif route == '#register':
            content = html.DIV([
                html.H1('Register'),
                html.FORM([
                    html.INPUT(type='text', placeholder='Full Name', id='fullName'),
                    html.INPUT(type='email', placeholder='Email', id='email'),
                    html.INPUT(type='text', placeholder='Designation', id='designation'),
                    html.INPUT(type='password', placeholder='Password', id='password'),
                    html.BUTTON('Register', type='submit')
                ], onSubmit=self.handle_register)
            ])
        elif route == '#dashboard':
            content = html.DIV([
                html.H1('Dashboard'),
                html.BUTTON('Create New POC', onClick=lambda: self.setState({'route': '#create-poc'})),
                html.DIV([
                    html.DIV([
                        html.H2('My Posted POCs'),
                        html.DIV([ 
                            html.DIV([
                                html.H3(poc['title'])
                            ], className='card') for poc in self.state['my_pocs']
                        ])
                    ], className='col'),
                    html.DIV([
                        html.H2('My Applications'),
                        html.DIV([
                            html.DIV([
                                html.P(f'Status: {app["status"]}')
                            ], className='card') for app in self.state['my_applications']
                        ])
                    ], className='col')
                ], className='row')
            ])
        elif route.startswith('#poc/'):
            poc = self.state['current_poc']
            if poc:
                content = html.DIV([
                    html.H1(poc['title']),
                    html.P(poc['description']),
                    html.P(f'Posted by: {poc["owner"]["full_name"]} ({poc["owner"]["designation"]})'),
                    html.H3('Comments'),
                    html.DIV([ 
                        html.DIV(f'{comment["author"]["full_name"]}: {comment["text"]}') for comment in self.state['comments']
                    ]),
                    html.FORM([
                        html.TEXTAREA(placeholder='Write a comment...', id='new-comment'),
                        html.BUTTON('Post Comment', type='submit')
                    ], onSubmit=self.handle_post_comment)
                ])
            else:
                content = html.H1('Loading POC...')
        elif route == '#create-poc':
            content = html.DIV([
                html.H1('Create New POC'),
                html.FORM([
                    html.INPUT(type='text', placeholder='Title', id='poc-title'),
                    html.TEXTAREA(placeholder='Description', id='poc-description'),
                    html.BUTTON('Create POC', type='submit')
                ], onSubmit=self.handle_create_poc)
            ])
        else:
            content = html.H1('404 Not Found')
        
        return html.DIV([nav, content])

    def handle_login(self, event):
        event.preventDefault()
        email = document['email'].value
        password = document['password'].value
        ajax.post('/token', data={'username': email, 'password': password}, oncomplete=self.on_login_complete)

    def on_login_complete(self, req):
        if req.status == 200:
            local_storage.setItem('token', req.json['access_token'])
            self.setState({'token': req.json['access_token'], 'route': '#dashboard'})
        else:
            alert('Login failed')

    def handle_register(self, event):
        event.preventDefault()
        fullName = document['fullName'].value
        email = document['email'].value
        designation = document['designation'].value
        password = document['password'].value
        ajax.post('/users', data={'full_name': fullName, 'email': email, 'designation': designation, 'password': password}, oncomplete=self.on_register_complete)

    def on_register_complete(self, req):
        if req.status == 200:
            window.location.hash = '#login'
        else:
            alert('Registration failed')

    def handle_post_comment(self, event):
        event.preventDefault()
        poc_id = self.state['route'].split('/')[1]
        text = document['new-comment'].value
        headers = {'Authorization': f'Bearer {self.state["token"]}'}
        ajax.post('/comments', headers=headers, data={'text': text, 'poc_id': int(poc_id)}, oncomplete=self.on_comment_posted)

    def on_comment_posted(self, req):
        if req.status == 200:
            self.fetch_poc_details(self.state['route'].split('/')[1])
        else:
            alert('Failed to post comment')

    def handle_create_poc(self, event):
        event.preventDefault()
        title = document['poc-title'].value
        description = document['poc-description'].value
        headers = {'Authorization': f'Bearer {self.state["token"]}'}
        ajax.post('/pocs', headers=headers, data={'title': title, 'description': description}, oncomplete=self.on_poc_created)

    def on_poc_created(self, req):
        if req.status == 200:
            self.setState({'route': '#dashboard'})
        else:
            alert('Failed to create POC')

react.render(App(), document.getElementById('app-root'))
