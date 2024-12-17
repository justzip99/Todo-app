from fastapi import APIRouter
from fastapi import HTTPException, status, Depends
from schemas.todo_schema import TodoGet, TodoPost, TodoPut
from models.todo_model import Todo
from settings.auth import verified_user

router = APIRouter(prefix="/api/v1", tags=["Todos"])


@router.get("/", dependencies=[Depends(verified_user)])
async def get_todos(user: dict = Depends(verified_user)):
    return await TodoGet.from_queryset(Todo.filter(user_id=user['user_id']).all())


@router.post("/",dependencies=[Depends(verified_user)])
async def create_todo(body: TodoPost,user: dict = Depends(verified_user)):
    data = body.model_dump(exclude_unset=True)
    data['user_id'] = user['user_id']
    todo = await Todo.create(**data)
    return await TodoGet.from_tortoise_orm(todo)


@router.put("/done/{todo_id}", dependencies=[Depends(verified_user)])
async def mark_done(todo_id: str, user: dict = Depends(verified_user)):
    todo_exists = await Todo.filter(id=todo_id, user_id=user['user_id']).exists()
    if not todo_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    await Todo.filter(id=todo_id, user_id=user['user_id']).update(done=True)
    return {"message": "Task marked as done"}

@router.put("/undone/{todo_id}", dependencies=[Depends(verified_user)])
async def mark_undone(todo_id: str, user: dict = Depends(verified_user)):
    todo_exists = await Todo.filter(id=todo_id, user_id=user['user_id']).exists()
    if not todo_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    await Todo.filter(id=todo_id, user_id=user['user_id']).update(done=False)
    return {"message": "Task marked as not done"}


@router.delete("/{todo_id}",dependencies=[Depends(verified_user)])
async def delete_todo(todo_id: str,user: dict = Depends(verified_user)):
    todo_exists = await Todo.filter(id=todo_id, user_id=user['user_id']).exists()
    if not todo_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    await Todo.filter(id=todo_id, user_id=user['user_id']).delete()
    return "Delete successful"
