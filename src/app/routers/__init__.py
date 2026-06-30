from . import index, auth, profile

routers = [
    index.router,
    auth.router,
    profile.router
]