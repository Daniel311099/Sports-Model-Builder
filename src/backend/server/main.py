import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from api.gql.schema import router as gql_router
from api.rest.router import router as rest_router

GQL_SUF = "/gql"
REST_SUF = "/rest"

app = FastAPI()
app.include_router(gql_router, prefix=GQL_SUF)
app.include_router(rest_router, prefix=REST_SUF)