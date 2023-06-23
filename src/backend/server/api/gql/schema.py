import strawberry

@strawberry.type
class Query:
    @ strawberry.field
    def hello(self) -> str:
        return "hello world!"

schema = strawberry.Schema(Query)    
