from django.urls import path, include, re_path

from ariadne_django.views import GraphQLView

from api.graphql.schema import schema


urlpatterns = [
    path('',
         GraphQLView.as_view(
             schema=schema,
         ),
         name='graphql'),
]