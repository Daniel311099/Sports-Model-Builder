from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from api.gql.schema import schema
from api.rest.router import router

GQL_SUF = "/gql"
REST_SUF = "/rest"

gql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(gql_app, prefix=GQL_SUF)
app.include_router(router, prefix=REST_SUF)