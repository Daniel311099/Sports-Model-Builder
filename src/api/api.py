import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Query:
    @ strawberry.field
    def hello(self) -> str:
        return "hello world!"

schema = strawberry.Schema(Query)    

gql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(gql_app, prefix="/hello")
