import cloudinary.uploader
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from users.services.users import update_user_profile_photo


@csrf_exempt
def user_profile_photo_upload_view(
        request: HttpRequest,
        user_id: int,
) -> HttpResponse:
    profile_photo: InMemoryUploadedFile | None = request.FILES.get(
        'profile_photo'
    )
    result = cloudinary.uploader.upload(profile_photo)
    profile_photo_url: str = result['secure_url']
    update_user_profile_photo(
        user_id=user_id,
        profile_photo_url=profile_photo_url,
    )
    return HttpResponse(status=status.HTTP_200_OK)
