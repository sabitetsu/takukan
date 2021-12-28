from django.urls import path
from . import views
from schedule.views import scheduleIndex, takusuke, takusukeIndex, UserView, PersonalSchedule

urlpatterns = [
    path('', views.scheduleIndex, name='scheduleIndex'),
    path('takusuke/',views.takusukeIndex, name='takusukeIndex'),
    # path('takusukeCreate/',views.takusukeCreate, name='takusukeCreate'),
    path('takusuke/<int:pk>',views.takusuke, name="takusuke"),
    # path('<str:pk>/',views.userSchedule, name='userSchedule'),
    path('user/<str:user>/',views.UserView.as_view(), name='userView'),
    # path('create/',views.UserTakuCreate.as_view(),name='userCreate'),
    path('pscreate/',views.PersonalScheduleCreate.as_view(),name='pscreate'),
]
