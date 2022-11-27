import graphene


class SectionType(graphene.ObjectType):
    name = graphene.String()
    description = graphene.String()
    threads = graphene.List('forum.ThreadType')


class ThreadType(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    created_by = graphene.Field('forum.UserType')
    posts = graphene.List('forum.PostType')
    open_date = graphene.DateTime()
    closed = graphene.Boolean()
    closing_date = graphene.DateTime()
    closed_by = graphene.Field('forum.UserType')
    section = graphene.Field(SectionType)


class PostType(graphene.ObjectType):
    user = graphene.Field('forum.UserType')
    thread = graphene.Field(ThreadType)
    content = graphene.String()
    datetime = graphene.DateTime()


class UserType(graphene.ObjectType):
    name = graphene.String()
    posts = graphene.List(PostType)
    threads_open = graphene.List(ThreadType)
    is_admin = graphene.Boolean()


class UniverseType(graphene.ObjectType):
    universe_id = graphene.Int()
    lang = graphene.String()
    name = graphene.String()


class Query:
    version = graphene.String()

    def resolve_version(self, info, **kwargs):
        return '0.0.0'
