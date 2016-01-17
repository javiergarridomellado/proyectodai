from django.conf.urls import patterns, url
from restaurante import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='about'),
		url(r'^menu/', views.menu, name='menu'),
		#url(r'^login/', views.login, name='auth_login'),
		#url(r'^bar/add_tapa/$', views.add_tapa, name='add_tapa'),#modificar esta ruta
		#url(r'^add_bar/$', views.add_tapa, name='add_tapa'),
		url(r'^bar/(?P<bar_name_slug>[\w\-]+)/$', views.bar, name='bar'),
		#url(r'^register/$', views.register, name='register'),
		url(r'^registro/$', views.register, name='registro'),
		url(r'^login/$', views.login_view, name='login'), 
		url(r'^restricted/', views.restricted, name='restricted'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^add_bar/$', views.add_bar, name='add_bar'),
		url(r'^bar/(?P<bar_name_slug>[\w\-]+)/add_tapa/$', views.add_tapa, name='add_tapa'),
		url(r'^reclama_datos/', views.reclama_datos, name='reclama_datos'),
		
)

from django.conf import settings # New Import
from django.conf.urls.static import static # New Import

#preguntar media
if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
