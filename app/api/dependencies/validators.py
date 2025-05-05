from app.api import models, schemas
from app.api.dependencies.exceptions import InternalServerError
from app.logger import logger


def validate_event_model(event: models.Event) -> schemas.event.Event:
    try:        
        if not event.first_team or not event.second_team:
            raise InternalServerError
        
        first_team = schemas.team.EventTeam.model_validate(event.first_team)
        second_team = schemas.team.EventTeam.model_validate(event.second_team)
        
        first_team.score = event.first_team_score
        second_team.score = event.second_team_score
        
        validated_event = schemas.event.Event(
            id=event.id, league=event.league, tour=event.tour, 
            start_date=event.start_date, end_date=event.end_date, 
            first_team=first_team, second_team=second_team,
            location_name=event.location.name if event.location else None,
            location_address=event.location.address if event.location else None
        )
        
        return validated_event
    except Exception as err:
        logger.error(err)
        raise InternalServerError