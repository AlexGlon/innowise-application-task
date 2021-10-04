"""innowise_application_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from attachments.views import AttachmentViewSet
from responses_comments.views import CommentViewSet, ResponseViewSet, ResponseByTicketView, CommentsThreadView
from tickets.views import UserViewSet, TicketViewSet, TicketsByUserView, TicketsByStatusView, \
    TicketsBySupportMemberView, TicketStatusUpdateView

router = routers.DefaultRouter()

# TODO: remove later
router.register(r'users', UserViewSet)

router.register(r'tickets', TicketViewSet)
# TODO: is there any way to rewrite this? low-key looks like garbage ngl
router.register(r'tickets/by_user/(?P<user>[^/.]+)', TicketsByUserView, basename='tickets-by-user')
router.register(r'tickets/by_status/(?P<ticket_status>[^/.]+)', TicketsByStatusView, basename='tickets-by-status')
router.register(r'tickets/by_support_member/(?P<support>[^/.]+)', TicketsBySupportMemberView,
                basename='tickets-by-support-member')
router.register(r'tickets/status_update', TicketStatusUpdateView, basename='ticket-status-update')

router.register(r'attachments', AttachmentViewSet)

router.register(r'responses', ResponseViewSet)

router.register(r'responses/(?P<pk>[^/.]+)/comments', CommentsThreadView, basename='response-comments')
router.register(r'responses/by_ticket/(?P<ticket_id>[^/.]+)', ResponseByTicketView, basename='response-by-ticket')

router.register(r'comments', CommentViewSet)

# swagger view
schema_view = get_swagger_view(title="Support desk API")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    url('swagger/', schema_view),
] + static(settings.MEDIA_URL)
