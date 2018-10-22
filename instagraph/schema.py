import graphene

import users.schema
import images.schema


class Query(users.schema.Query, images.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
