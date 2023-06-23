from fastapi import APIRouter

from .resolvers import test_resolver

router = APIRouter()

endpoints = {
    'test': test_resolver
}

for endpoint, resolver in endpoints.items():
    router.get(f'/{endpoint}')(resolver)
