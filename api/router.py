from rest_framework import routers
from .views.py import *

router = routers.DefaultRouter()
router.register(r'user/images': get_user_image)
