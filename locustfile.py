
# Documentation http://docs.locust.io/en/stable/index.html
# pip install locust
# To start in the terminal, type the command "Locust"


from locust import HttpUser, task
from random import randint


class SetTasks(HttpUser):
    url = 'http://127.0.0.1:8000/api/%s'

    count_author_obj = 400
    count_book_obj = 1500

    created_book = list()

    @task(10)  # takes an optional argument that can be used to indicate the importance of the task.
    def get_authors(self):
        self.client.get(self.url % 'authors/')

    @task(7)
    def retrieve_author(self):
        self.client.get(self.url % f'authors/{randint(1, self.count_author_obj)}')

    @task(10)
    def get_books(self):
        self.client.get(self.url % f'books/')

    @task(7)
    def retrieve_book(self):
        self.client.get(self.url % f'books/{randint(1, self.count_book_obj)}')

    @task(3)
    def create_book(self):
        data = {
            'author': randint(1, self.count_author_obj),
            'name': 'book_stress_test',
            'description': f'{"Text text text" * randint(5, 15)}',
            'release_date': '1750-05-19'
        }

        response = self.client.post(self.url % f'books/', data=data)
        try:
            self.created_book.append(response.json()['id'])
        except:  # NOQA
            pass

    @task(2)
    def update_book(self):
        data = {'description': f'{"Text text text" * randint(5, 15)}'}

        self.client.patch(self.url % f'books/{randint(1, self.count_author_obj)}/', data=data)

    @task(1)
    def delete_book(self):
        try:
            book = self.created_book.pop(randint(0, len(self.created_book)))
            self.client.delete(self.url % f'books/{book}/',)
        except:  # NOQA
            pass
