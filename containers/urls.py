from django.urls import path, re_path
from main.views import (Dashboard, CourierAccountLogin,
 CourierAccountRegister, Homepage)
from . import views
from containers.views import *

app_name = 'containers'

urlpatterns = [
    path('container/', ContainerView.as_view(), name='container'),
    path('listpackages/', ListContainers.as_view(), name='listpackages'), # list out the containers
    path('updatepackages/<int:id>', views.container_update, name='updatepackages'),
    path('remove_container/<int:id>', views.remove_container, name='remove_container'),
    path('containerdetailedview/<int:id>', views.containerDetailedView, name='containerdetailedview'),
    path('printoutcontainerdetailedview/<int:id>', views.printoutContainerDetailedView, name='printoutcontainerdetailedview'),
    # updating existing item
    path('extra-details/<str:ref>', views.addExtraToContainerRegistered, name='extra-details'),
    # adding extra item to already existing item
    path('extra-details-more/<str:ref>', views.extraDetailsMore, name='extra-details-more'),
    # remove items
    path('remove-items/<int:id>', views.removeItems, name='remove-items'),

     # 
    path('task/', views.taskPage, name='task'),
    path('removetask/', views.removeTask, name='removetask'),
    path('automatetask/', views.automateTask, name='automatetask'),
    # update the task staus, if is pending,received or rejected,
    # this will have a javascript post request with data.
    # take a look at the container > template > list_task.html
    path('taskstatus/', views.taskStatus, name='taskstatus'),
  


]