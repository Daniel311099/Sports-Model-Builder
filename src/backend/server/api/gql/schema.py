import strawberry

from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Query:
    @ strawberry.field
    def hello(self) -> str:
        return "hello world!"

schema = strawberry.Schema(Query)    

router = GraphQLRouter(schema)