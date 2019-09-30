from io import BytesIO
from django.http import JsonResponse
from django.views import View
from infra.request.errors import BadRequestError
from infra.views import BaseView
from image_medias.models.image_media import ImageMedia
from helpers.view_helpers import requirejwt


class MediasResourceView(View):

    def post(self, request):
        view = UploadMediaView()
        return view(request)


class UploadMediaView(BaseView):

    @requirejwt
    def validate(self, request):
        if not request.content_type == 'application/octet-stream':
            raise BadRequestError('Content type must be octet-stream.')

    def run(self, request):
        data = BytesIO(request.body)
        image_media = ImageMedia.objects.create(user_id=self.user_payload['id'])
        image_media.upload_image(data)
        return JsonResponse(image_media.serialized)