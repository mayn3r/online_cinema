from . import auth, pages, profile, admin

routers = [
    pages.router,
    admin.router,
    auth.router,
    profile.router
]