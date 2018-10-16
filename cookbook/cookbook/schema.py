import graphene

from ingredients.schema import Query

class Query(Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
