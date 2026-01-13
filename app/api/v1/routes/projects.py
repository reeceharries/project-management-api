from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from app.db.dependencies import SessionDep
from app.models import Project
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: ProjectCreate, session: SessionDep):
    project = Project(**project_in.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.get("/", response_model=list[ProjectRead])
async def read_projects(session: SessionDep):
    result = await session.execute(select(Project))
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(project_id: int, session: SessionDep):
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
        project_id: int,
        project_in: ProjectUpdate,
        session: SessionDep,
):
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, session: SessionDep):
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(project)
    await session.commit()
