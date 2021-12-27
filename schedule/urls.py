from django.urls import path
from . import views
from schedule.views import scheduleIndex, userSchedule, takusuke, takusukeIndex

urlpatterns = [
    path('', views.scheduleIndex, name='scheduleIndex'),
    path('takusuke/',views.takusukeIndex, name='takusukeIndex'),
    # path('takusukeCreate/',views.takusukeCreate, name='takusukeCreate'),
    path('takusuke/<int:pk>',views.takusuke, name="takusuke"),
    path('<str:pk>/',views.userSchedule, name='userSchedule'),
]
