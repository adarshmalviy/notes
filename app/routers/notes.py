from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.database.models import Notes, SharedNoteToUser, User
from app.authentication.auth_bearer import JWTBearer
from app.authentication.dependencies import current_user
from app.schemas.notes import NoteCreate, NoteSearchResult, NoteUpdate, ShareToUser
from tortoise.expressions import Q
router = APIRouter()

@router.get("", dependencies=[Depends(JWTBearer())])
async def get_all_notes(user=Depends(current_user)):
    try:
        notes = await Notes.filter(user=user).all()
        shared_notes_user = await SharedNoteToUser.filter(recipient_user=user).all().prefetch_related('note')
        shared_notes=[]
        for note in shared_notes_user:
            shared_notes.append(note.note)
            
        return {"message": "success", "notes": notes, "shared_notes":shared_notes}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{note_id}", dependencies=[Depends(JWTBearer())])
async def get_note_by_id(note_id: int, user=Depends(current_user)):
    try:
        note = await Notes.filter(id=note_id, user=user).first()
        if not note:
            shared_note = await SharedNoteToUser.get_or_none(note_id=note_id, recipient_user=user).prefetch_related('note')
            if shared_note:
                return {"message": "success", "note": shared_note.note} 
            raise HTTPException(status_code=404, detail="Note not found")
        
        return {"message": "success", "note": note}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", dependencies=[Depends(JWTBearer())])
async def create_note(note_data: NoteCreate, user=Depends(current_user)):
    try:
        new_note = await Notes.create(
            title=note_data.title,
            content=note_data.content,
            user=user
        )
        return {"message": "success", "note_id": new_note.id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{note_id}", dependencies=[Depends(JWTBearer())])
async def update_note(note_id: int, note_data: NoteUpdate, user=Depends(current_user)):
    try:
        note = await Notes.filter(id=note_id, user=user).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        for field in ['title', 'content']:
            if hasattr(note_data, field):
                value = getattr(note_data, field, None)
                if value is not None:
                    setattr(note, field, value)
        
        await note.save()

        return {"message": "success"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{note_id}", dependencies=[Depends(JWTBearer())])
async def delete_note(note_id: int, user=Depends(current_user)):
    try:
        note = await Notes.filter(id=note_id, user=user).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        await note.delete()
        return {"message": "success"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{note_id}/share", dependencies=[Depends(JWTBearer())])
async def share_note(
    note_id: int, share_data: ShareToUser, request: Request, user=Depends(current_user)
):
    try:
        # Check if the note exists and belongs to the authenticated user
        note = await Notes.filter(id=note_id, user=user).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        # Check if the recipient user exists
        recipient_user = await User.filter(username=share_data.recipient_username).first()
        if not recipient_user:
            raise HTTPException(status_code=404, detail="Recipient user not found")

        # Check if the note is already shared with the recipient
        shared_note = await SharedNoteToUser.filter(note=note, recipient_user=recipient_user).first()
        if shared_note:
            raise HTTPException(status_code=400, detail="Note already shared with the recipient user")

        # Share the note
        await SharedNoteToUser.create(note=note, recipient_user=recipient_user)

        return {"message": "success"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/note/search", dependencies=[Depends(JWTBearer())])
async def search_notes(
    q: str = Query(..., min_length=1, description="Search query"),
    user:User=Depends(current_user),
):
    try:

        # Search for notes based on keywords in the title or content
        search_results = await Notes.filter(
            Q(title__icontains=q, content__icontains=q, join_type="OR"), user=user).all()

        # Search for notes shared with the user based on keywords in the title or content
        shared_notes = await SharedNoteToUser.filter(
            Q(note__title__icontains=q, note__content__icontains=q, join_type="OR"),
            recipient_user=user
        ).all().prefetch_related('note')
        
        print(search_results)
        # Convert the search results to a list of NoteSearchResult objects
        search_results_list = [
            NoteSearchResult(id=note.id, title=note.title, content=note.content)
            for note in search_results
        ] + [
            NoteSearchResult(id=shared_note.note.id, title=shared_note.note.title, content=shared_note.note.content)
            for shared_note in shared_notes
        ]
        
        return {"message": "success", "search_results": search_results_list}
    except HTTPException as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

