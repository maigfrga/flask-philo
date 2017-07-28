from flask import request
from flaskutils import app
from flaskutils.views import BaseResourceView


class ExampleView(BaseResourceView):
    def get(self):
        return self.json_response(
            status=200, data={'some_data': 'yes'})
