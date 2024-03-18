from pyramid.view import view_config
from sqlalchemy import select

from aramaki.models.observation import Observation


@view_config(
    route_name="dashboard",
    renderer="aramaki.web:templates/dashboard.pt",
)
def dashboard(request):
    observations = request.dbsession.scalars(
        select(Observation).filter_by(
            system_id="4f607f0e-ba0f-4d9a-93bf-f9c6dbfcaf99"
        )
    )

    return {"observations": list(observations)}
