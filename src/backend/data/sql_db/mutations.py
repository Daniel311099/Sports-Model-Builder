from prisma import Prisma
from prisma.types import UserCreateInput

class Mutations:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    def create_user(self, user: UserCreateInput):
        return self.prisma.user.create(user)