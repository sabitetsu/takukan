from django.urls import path
from . import views
from schedule.views import scheduleIndex, takusuke, takusukeIndex, UserView, PersonalScheduleCreate, PersonalScheduleUpdate

urlpatterns = [
    path('', views.scheduleIndex, name='scheduleIndex'),
    path('takusuke/',views.takusukeIndex, name='takusukeIndex'),
    path('takusuke/<int:pk>',views.takusuke, name="takusuke"),
    path('user/<str:user>/',views.UserView.as_view(), name='userView'),
    path('pscreate/',views.PersonalScheduleCreate.as_view(),name='pscreate'),
    path('psupdate/<int:pk>',views.PersonalScheduleUpdate.as_view(),name='psupdate'),
]
