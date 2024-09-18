from django.contrib import admin
from django.urls import path
from videos.views import upload_video, search_subtitles, video_list, upload_success, video_detail
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_video, name='upload_video'),
    path('search/', search_subtitles, name='search_subtitles'),
    path('videos_list/', video_list, name='video_list'),  # List of all videos
    path('videos/<int:video_id>/', video_detail, name='video_detail'),  # Video detail view
    path('upload/success/', upload_success, name='upload_success'),  # Success page

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
