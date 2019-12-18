import json
import pytest
from django.test import Client
from helpers.testing_helpers import get_fake_jwt_request
from models.views.model_views.create_model_view import CreateModelView
from models.tests.factories.category_factory import CategoryFactory
from models.models.model import Model
from infra.request.errors import (
    ForbiddenError,
    BadRequestError,
)
from users.tests.factories.user_factory import UserFactory
from users.models.user import User
from model_medias.tests.factories.model_media_factory import ModelMediaFactory


@pytest.mark.django_db
class TestCreateModelView:

    def test_validate_not_valid_content_type(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        request = get_fake_jwt_request(user=user, content_type='not valid ct')
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_body_is_provided_on_request(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        request = get_fake_jwt_request(user)
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_privacy_is_not_provided(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy']
        request = get_fake_jwt_request(user, body=json.dumps({'user': 1, 'name': 'Model name', 'model_media': 1}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_user_is_not_provided(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy']
        request = get_fake_jwt_request(user, body=json.dumps({'privacy': 1, 'name': 'Model name', 'model_media': 1}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_name_is_not_provided(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy']
        request = get_fake_jwt_request(user, body=json.dumps({'user': 1, 'privacy': 1, 'model_media': 1}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_model_media_is_not_provided(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy']
        request = get_fake_jwt_request(user, body=json.dumps({'user': 1, 'privacy': 1, 'name': 'model name'}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_user_id(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()

        request = get_fake_jwt_request(user, body=json.dumps({
            'user': -1,
            'privacy': 1,
            'name': 'model name',
            'model_media': 1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_model_media(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': -1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_privacy(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        model_media = ModelMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': -1,
            'name': 'model name',
            'model_media': model_media.id,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_category(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        model_media = ModelMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'category': -1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_user_try_to_create_model_for_other_user_and_no_permissions(self):
        user = UserFactory(access_level=User.Type.COMMON_USER_TYPE)
        user_two = UserFactory()
        view = CreateModelView()
        model_media = ModelMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user_two.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
        }))
        with pytest.raises(ForbiddenError):
            view.validate(request)

    def test_run_create_and_return_object(self):
        user = UserFactory(access_level=User.Type.COMMON_USER_TYPE)
        view = CreateModelView()
        model_media = ModelMediaFactory()
        category = CategoryFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'description': 'So good description',
            'category': category.id,
        }))
        response = view.run(request)
        assert response.status_code == 200
        response_body = json.loads(response.content)
        assert response_body['user'] == user.id
        assert response_body['privacy'] == 1
        assert response_body['name'] == 'model name'
        assert response_body['model_media'] == model_media.id
        assert response_body['description'] == 'So good description'
        assert response_body['category'] == category.id
        assert Model.objects.filter(id=response_body['id']).exists() is True


@pytest.mark.django_db
class TestCreateModelViewIntegration():

    def test_create_model(self):
        user = UserFactory(access_level=User.Type.COMMON_USER_TYPE)
        model_media = ModelMediaFactory()
        category = CategoryFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        data = {
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'description': 'So good description',
            'category': category.id,
        }
        response = Client().post('/models/', data, content_type='application/json', **headers)
        assert response.status_code == 200
        assert response.json().get('user') == user.id