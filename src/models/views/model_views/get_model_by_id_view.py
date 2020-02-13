from django.http import JsonResponse
from infra.request.errors import (
    NotFoundError,
    ForbiddenError,
)
from infra.views import BaseView
from models.models.model import Model
from helpers.view_helpers import require_jwt
from django.db.models import Q
from users.models.user import User


class GetModelByIdView(BaseView):

    @require_jwt
    def validate(self, request, model_id, *args, **kwargs):
        super().validate(request, model_id, *args, **kwargs)
        if not Model.objects.filter(id=model_id).exists():
            raise NotFoundError('The provided model id does not exists')
        if self.user_payload['access_level'] > User.Type.COMMON_USER_TYPE.value:
            return
        if Model.objects.filter(
            Q(id=model_id),
            Q(privacy=Model.Privacy.PRIVATE.value),
            ~Q(user_id=self.user_payload['id']),
        ).exists():
            raise ForbiddenError()

    def run(self, request, model_id, *args, **kwargs):
        return JsonResponse(Model.objects.get(id=model_id).serialized)
