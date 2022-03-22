from django.urls import path, include, re_path
from web.settings import DEBUG

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from ariadne_django.views import GraphQLView

from api.views import LoginView, APICategoriesViewSet, APIManufacturersViewSet, APIProductsViewSet, APIOrdersViewSet,\
    APIUsersViewSet
from api.graphql.schema import schema

router = routers.DefaultRouter()

api = routers.DefaultRouter() if DEBUG else routers.SimpleRouter()
api.register(r'Users', APIUsersViewSet)
api.register(r'Categories', APICategoriesViewSet)
api.register(r'Manufacturers', APIManufacturersViewSet)
api.register(r'Products', APIProductsViewSet)
api.register(r'Orders', APIOrdersViewSet)

schema_view = get_swagger_view(title='Nnicrow online-shop API')

urlpatterns = [
    # path('', include(router.urls)),
    path('api/rest-api/', include(api.urls)),
    path('rest-api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/api-login/', LoginView.as_view(), name='api-login'),
    re_path(r'^swagger/$', schema_view),
    path('',
         GraphQLView.as_view(
             schema=schema,
         ),
         name='graphql'),
]