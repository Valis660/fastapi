from src.repositories.base import BaseRepositoriy
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepositoriy):
    model = RoomsOrm
