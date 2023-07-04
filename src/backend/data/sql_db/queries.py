from prisma import Prisma

class Queries:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    def get_user(self, user_id: int):
        return self.prisma.user.find_unique(where={'id': user_id})