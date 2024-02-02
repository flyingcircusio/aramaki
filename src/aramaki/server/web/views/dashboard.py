from pyramid.view import view_config


@view_config(
    route_name="dashboard",
    renderer="aramaki.server.web:templates/dashboard.pt",
)
def dashboard(request):
    return {}
