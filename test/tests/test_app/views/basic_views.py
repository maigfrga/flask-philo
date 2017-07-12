from flask import request
from flaskutils import app
from flaskutils.views import BaseView, BaseResourceView
from pgsqlutils.base import Session
from pgsqlutils.exceptions import NotFoundError

from .models import User

from .serializers import (
    GetUserSerializer, PostUserSerializer, PutUserSerializer
)


class BasicHTMLView(BaseView):
    def get(self):
        return self.render_template('home.html')


class UserResourceView(BaseResourceView):

    def get(self, id=None):
        try:
            if not id:
                data = [
                    GetUserSerializer(model=user).to_json()
                    for user in User.objects.filter_by()
                ]
            else:
                data = GetUserSerializer(
                    model=User.objects.get(id=id)).to_json()

            return self.json_response(data=data)
        except NotFoundError:
            return self.json_response(status=400)

    def post(self):
        try:
            serializer = PostUserSerializer(request=request)
            user = User(serializer=serializer)
            user.add()
            Session.commit()
            user = User.objects.get(id=user.id)
            app.logger.info('user with id {} has been created'.format(user.id))
            return self.json_response(status=201, data={'id': user.id})

        except Exception as e:
            app.logger.error(e)
            Session.rollback()
            return self.json_response(status=500)

    def put(self, id):
        try:
            serializer = PutUserSerializer(request=request)
            user = User(serializer=serializer)
            user.update()
            Session.commit()
            return self.json_response(
                status=200, data=PutUserSerializer(model=user).to_json())
        except Exception as e:
            app.logger.error(e)
            Session.rollback()
            return self.json_response(status=500)

    def delete(self, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            Session.commit()
            return self.json_response()
        except Exception as e:
            app.logger.error(e)
            Session.rollback()
            return self.json_response(status=500)
