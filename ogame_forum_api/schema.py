import graphene
import forum.schema


class Query(forum.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
