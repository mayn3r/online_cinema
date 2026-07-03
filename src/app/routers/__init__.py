from . import auth, pages, profile, admin, watchlist

routers = [
    pages.router,
    admin.router,
    auth.router,
    profile.router,
    watchlist.router
]