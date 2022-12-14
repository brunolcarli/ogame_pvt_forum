from datetime import datetime
import graphene
from forum.models import Section, Thread, Post, CustomUser
from forum.auth import access_required


class SectionType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    threads = graphene.List('forum.schema.ThreadType')

    def resolve_threads(self, info, **kwargs):
        return self.thread_set.all()


class ThreadType(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    content = graphene.String()
    created_by = graphene.Field('forum.schema.UserType')
    posts = graphene.List('forum.schema.PostType')
    open_date = graphene.DateTime()
    closed = graphene.Boolean()
    closing_date = graphene.DateTime()
    closed_by = graphene.Field('forum.schema.UserType')
    section = graphene.Field(SectionType)
    last_post_datetime = graphene.DateTime()

    def resolve_posts(self, info, **kwargs):
        return self.post_set.all()


class PostType(graphene.ObjectType):
    id = graphene.ID()
    user = graphene.Field('forum.schema.UserType')
    thread = graphene.Field(ThreadType)
    content = graphene.String()
    datetime = graphene.DateTime()


class UserType(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    posts = graphene.List(PostType)
    threads_open = graphene.List(ThreadType)
    is_superuser = graphene.Boolean()
    bio = graphene.String()
    avatar = graphene.String()
    date_joined = graphene.DateTime()
    posts_count = graphene.Int()
    threads_count = graphene.Int()
    last_activity = graphene.DateTime()
    is_banned = graphene.Boolean()

    def resolve_posts(self, info, **kwargs):
        return self.posted_by.all()

    def resolve_threads_open(self, info, **kwargs):
        return self.thread_creator.all()

    def resolve_posts_count(self, info, **kwargs):
        return self.posted_by.count()

    def resolve_threads_count(self, info, **kwargs):
        return self.thread_creator.count()


class UniverseType(graphene.ObjectType):
    universe_id = graphene.Int()
    lang = graphene.String()
    name = graphene.String()


########################
#  QUERY
########################

class Query:
    version = graphene.String()

    def resolve_version(self, info, **kwargs):
        return '0.0.6'

    #######################
    #  Multiple objects
    #######################

    # Query users
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return CustomUser.objects.filter(**kwargs)

    # Query Sections
    sections = graphene.List(SectionType)

    def resolve_sections(self, info, **kwargs):
        return Section.objects.filter(**kwargs)

    # Query Threads
    threads = graphene.List(ThreadType)

    def resolve_threads(self, info, **kwargs):
        return Thread.objects.filter(**kwargs)

    # Query Posts
    posts = graphene.List(PostType)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.filter(**kwargs)

    #######################
    #  Single objects
    #######################

    # Users
    user = graphene.Field(
        UserType,
        id=graphene.ID(required=True)
    )

    def resolve_user(self, info, **kwargs):
        try:
            user = CustomUser.objects.get(**kwargs)
        except CustomUser.DoesNotExist:
            raise Exception('QUERY ERROR: Requested object not found!')
        return user

    # Section
    section = graphene.Field(
        SectionType,
        id=graphene.ID(required=True)
    )

    def resolve_section(self, info, **kwargs):
        try:
            section = Section.objects.get(**kwargs)
        except Section.DoesNotExist:
            raise Exception('QUERY ERROR: Requested object not found!')

        return section

    # Thread
    thread = graphene.Field(
        ThreadType,
        id=graphene.ID(required=True)
    )

    def resolve_thread(self, info, **kwargs):
        try:
            thread = Thread.objects.get(**kwargs)
        except Thread.DoesNotExist:
            raise Exception('QUERY ERROR: Requested object not found!')

        return thread


#####################
#  MUTATIONS
#####################

class CreateSection(graphene.relay.ClientIDMutation):
    section = graphene.Field(SectionType)

    class Input:
        username = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        user = CustomUser.objects.get(id=kwargs['user_id'])
        if not user.is_superuser:
            raise Exception('ERROR: Unauthorized')

        section, created = Section.objects.get_or_create(name=kwargs['name'])

        if not created:
            raise Exception('ERROR: Section name already created.')

        section.description = kwargs['description']
        section.save()

        return CreateSection(section)


class CreateThread(graphene.relay.ClientIDMutation):
    thread = graphene.Field(ThreadType)

    class Input:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        username = graphene.ID(required=True)
        section_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            section = Section.objects.get(id=kwargs['section_id'])
        except Section.DoesNotExist:
            raise Exception('ERROR: Invalid or inexistent section.')

        try:
            user = CustomUser.objects.get(id=kwargs['user_id'])
        except CustomUser.DoesNotExist:
            raise Exception('ERROR: Invalid or inexistent user.')

        thread = Thread.objects.create(
            title=kwargs['title'],
            content=kwargs['content'],
            section=section,
            created_by=user
        )
        thread.save()
        user.last_activity = datetime.utcnow()
        user.save()

        return CreateThread(thread)


class CreatePost(graphene.relay.ClientIDMutation):
    post = graphene.Field(PostType)

    class Input:
        content = graphene.String(required=True)
        username = graphene.ID(required=True)
        thread_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        try:
            thread = Thread.objects.get(id=kwargs['thread_id'])
        except Thread.DoesNotExist:
            raise Exception('ERROR: Invalid or inexistent thread.')

        try:
            user = CustomUser.objects.get(id=kwargs['user_id'])
        except CustomUser.DoesNotExist:
            raise Exception('ERROR: Invalid or inexistent user.')


        post = Post.objects.create(
            user=user,
            thread=thread,
            content=kwargs['content']
        )
        post.save()
        thread.last_post_datetime = datetime.utcnow()
        thread.save()
        user.last_activity = datetime.utcnow()
        user.save()

        return CreatePost(post)


class CreateUser(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        bio = graphene.String()
        avatar = graphene.String()

    def mutate_and_get_payload(self, info, **kwargs):

        try:
            user = CustomUser.objects.get(username=kwargs['username'])
        except CustomUser.DoesNotExist:
            # Username free to use
            pass
        else:
            raise Exception('ERROR: username already in use!')

        user, created = CustomUser.objects.get_or_create(email=kwargs['email'])
        if not created:
            raise Exception('ERROR: email already registered!')

        user.username = kwargs['username']
        user.bio = kwargs.get('bio', '')
        user.avatar = kwargs.get(
            'avatar',
            'https://www.baxterip.com.au/wp-content/uploads/2019/02/anonymous.jpg'
        )
        user.last_activity = datetime.utcnow()
        try:
            user.set_password(kwargs['password'])
            user.save()
        except:
            pass

        return CreateUser(user)


class Mutation:
    create_section = CreateSection.Field()
    create_thread = CreateThread.Field()
    create_post = CreatePost.Field()
    create_user = CreateUser.Field()
