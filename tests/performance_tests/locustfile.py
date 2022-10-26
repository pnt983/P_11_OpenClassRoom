from locust import HttpUser, task


class Gudlft(HttpUser):
    
    @task
    def index(self):
        self.client.get('/')

    @task
    def showSummary(self):
        self.client.post('/showSummary', data = {'email': 'john@simplylift.co'})

    @task
    def book(self):
        self.client.get('/book/Spring%20Festival/Simply%20Lift')

    @task
    def purchasePlaces(self):
        self.client.post('/purchasePlaces', data = {'competition': 'Spring Festival',
                                                    'club': 'Simply Lift',
                                                    'places': 9})
    
    @task
    def display_points(self):
        self.client.get('/displayPoints')

    @task
    def logout(self):
        self.cleint.get('/logout')

