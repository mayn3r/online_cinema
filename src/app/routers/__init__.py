from . import index, auth, profile, admin

routers = [
    index.router,
    admin.router,
    auth.router,
    profile.router
]