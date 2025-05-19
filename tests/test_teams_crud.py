from unittest.mock import patch

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cruds import team as crud
from app.api.cruds.team import get_team_by_id
from app.api.dependencies.exceptions import TeamNotFound
from app.api import models
from app.api.schemas.team import CreateTeam, Team
from app.api.services.teams_service import (create_team, delete_team,
                                            edit_team, get_team)
from app.api.schemas.user import User
from app.api.services.users_service import check_user_permission
from app.config import transactions


@pytest.mark.asyncio
async def test_create_team(session: AsyncSession):
    team = await crud.create_team(session, name="Test team", logo_url="http://example.com")
    result = await crud.get_team_by_id(session, team.id)

    assert result.id == team.id
    assert result.name == team.name


@pytest.mark.asyncio
async def test_get_team_success(session: AsyncSession):
    result = await crud.get_team_by_id(session, 1)

    assert result.id == 1
    assert result.name == "Test team"


@pytest.mark.asyncio
async def test_get_team_not_found(session: AsyncSession):
    result = await crud.get_team_by_id(session, 999)
    
    assert result is None
        

@pytest.mark.asyncio
async def test_get_all_teams(session: AsyncSession):
    await crud.create_team(session, name="Test team", logo_url="http://example.com")    
    
    teams = await crud.get_all_teams(session, limit=10, offset=0)
    
    teams_obj_orm = [Team.model_validate(team) for team in teams]
    
    teams_obj = [
        Team.model_validate({"id": 1, "name": "Test team", "logo_url": "http://example.com"}),
        Team.model_validate({"id": 2, "name": "Test team", "logo_url": "http://example.com"}),
    ]
    
    assert teams_obj_orm == teams_obj


@pytest.mark.asyncio
async def test_edit_team_name(session: AsyncSession):
    team = await crud.get_team_by_id(session, 1)
    team = await crud.edit_team(session, team, name="Edited team")
    
    assert team.name == "Edited team"
    

@pytest.mark.asyncio
async def test_edit_team_logo_url(session: AsyncSession):
    team = await crud.get_team_by_id(session, 1)
    team = await crud.edit_team(session, team, logo_url="http://edited_example.com")
    
    assert team.logo_url == "http://edited_example.com"
    

@pytest.mark.asyncio
async def test_edit_team(session: AsyncSession):
    team = await crud.get_team_by_id(session, 2)
    team = await crud.edit_team(
        session, team, name="Edited team", logo_url="http://edited_example.com"
    )
    
    assert team.name == "Edited team"
    assert team.logo_url == "http://edited_example.com"


@pytest.mark.asyncio
async def test_delete_team(session: AsyncSession):
    team = await crud.get_team_by_id(session, 1)
    
    await crud.delete_team(session, team)
    
    team = await crud.get_team_by_id(session, 1)
    
    assert team is None