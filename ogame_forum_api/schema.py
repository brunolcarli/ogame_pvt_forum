import graphene
import forum.schema
import graphql_jwt


class Query(forum.schema.Query, graphene.ObjectType):
    pass


class Mutation(forum.schema.Mutation, graphene.ObjectType):
    log_in = graphql_jwt.ObtainJSONWebToken.Field()
    validate_user_token = graphql_jwt.Verify.Field()
    refresh_user_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
