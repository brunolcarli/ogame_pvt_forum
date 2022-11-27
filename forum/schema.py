import graphene


class Query:
    version = graphene.String()

    def resolve_version(self, info, **kwargs):
        return '0.0.0'
