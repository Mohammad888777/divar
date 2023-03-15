import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import OriginValidator,AllowedHostsOriginValidator


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


django_asgi_app = get_asgi_application()

# import echo.routing
import core.routing


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
                        "websocket": 

                        # OriginValidator(

                            SessionMiddlewareStack(
                                
                                    AllowedHostsOriginValidator(

                                            AuthMiddlewareStack(URLRouter( core.routing.websocket_urlpatterns))
                                
                                )

                            # )
                            ),
    }
)
