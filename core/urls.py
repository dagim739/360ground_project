from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.log_in, name='log_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addevents/', views.addevents, name='addevents'),
    path('addrecurringevent/', views.addrecurringevent, name='addrecurringevent'),
    path('editevent/', views.editevent, name='editevent'),
    path('editcomplete/', views.editcomplete, name='editcomplete'),
    path('deleteevent/', views.deleteevent, name='deleteevent'),
    path('addeventsafterreg/', views.addeventsafterreg, name='addeventsafterreg'),
    path('changeform/', views.changeform, name='changeform'),
    path('changerecurrenceform/', views.changerecurrenceform, name='changerecurrenceform'),
    path('profile/', views.profile, name='profile'),
    path('changeusername/', views.changeusername, name='changeusername'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('logout/', views.logout, name='logout'),
]