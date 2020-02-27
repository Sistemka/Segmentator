from app.app import api
from app.handlers import (
    errors,
    manage
)

manage.register(api)
errors.register()
