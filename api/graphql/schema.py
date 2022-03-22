from ariadne import ObjectType, gql, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL

from api.graphql.resolver import QueryResolver, CategoriesResolver, ManufacturersResolver, ProductsResolver, \
    SliderResolver, MutationResolver, BasketResolver

type_defs = gql(load_schema_from_path("api/graphql/schema.graphql"))

schema = make_executable_schema(
    type_defs,
    QueryResolver.query,
    CategoriesResolver.categories,
    ManufacturersResolver.manufacturers,
    ProductsResolver.products,
    SliderResolver.slider,
    MutationResolver.mutation,
    BasketResolver.basket
)

app = GraphQL(schema, debug=False)
