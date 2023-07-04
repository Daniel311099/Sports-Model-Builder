from prisma import Prisma

from queries import Queries
from mutations import Mutations

class DB:
    def __init__(self):
        self.prisma = Prisma()
        self.query = Queries(self.prisma)
        self.mutation = Mutations(self.prisma)