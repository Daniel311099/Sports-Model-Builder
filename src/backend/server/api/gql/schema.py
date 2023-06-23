import strawberry

from .resolvers import gql_test

@strawberry.type
class Query:
    test = strawberry.field(gql_test)
    
schema = strawberry.Schema(Query)    
