from src.repositories.base import BaseRepositoriy
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepositoriy):
    model = HotelsOrm
