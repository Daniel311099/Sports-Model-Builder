import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from api.gql.schema import schema
from api.rest.router import router

gql_app = GraphQLRouter(schema)

GQL_SUF = "/gql"
REST_SUF = "/rest"

app = FastAPI()
app.include_router(gql_app, prefix=GQL_SUF)
app.include_router(router, prefix=REST_SUF)