from flask import Blueprint

from services.RatingsService import RatingsService

courses_service = RatingsService()

route = Blueprint("ratings", __name__)

# #########
# ###GET###
# #########


# ########
# ##POST##
# ########