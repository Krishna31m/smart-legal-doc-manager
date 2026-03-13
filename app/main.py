from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud, diff_utils
from .tasks import check_change

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Legal Document Manager")


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/documents")
def create_document(data: schemas.DocumentCreate, db: Session = Depends(get_db)):

    doc = crud.create_document(db, data.title, data.content, data.user)

    return {"document_id": doc.id}


@app.post("/documents/{doc_id}/versions")
def add_version(doc_id: str, data: schemas.VersionCreate, db: Session = Depends(get_db)):

    latest = crud.get_latest_version(db, doc_id)

    new_version = models.DocumentVersion(
        document_id=doc_id,
        content=data.content,
        version_number=latest.version_number + 1,
        modified_by=data.user
    )

    db.add(new_version)
    db.commit()

    check_change.delay(latest.content, data.content, doc_id)

    return {"message": "version created"}


@app.get("/documents/{doc_id}/compare")
def compare(doc_id: str, v1: int, v2: int, db: Session = Depends(get_db)):

    version1 = db.query(models.DocumentVersion)\
        .filter(models.DocumentVersion.document_id == doc_id,
                models.DocumentVersion.version_number == v1).first()

    version2 = db.query(models.DocumentVersion)\
        .filter(models.DocumentVersion.document_id == doc_id,
                models.DocumentVersion.version_number == v2).first()

    diff = diff_utils.compare_versions(version1.content, version2.content)

    return {"diff": diff}


@app.patch("/documents/{doc_id}")
def update_title(doc_id: str, data: schemas.TitleUpdate, db: Session = Depends(get_db)):

    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()

    doc.title = data.title
    db.commit()

    return {"message": "title updated"}


@app.delete("/documents/{doc_id}/versions/{version}")
def delete_version(doc_id: str, version: int, db: Session = Depends(get_db)):

    v = db.query(models.DocumentVersion)\
        .filter(models.DocumentVersion.document_id == doc_id,
                models.DocumentVersion.version_number == version).first()

    db.delete(v)
    db.commit()

    return {"message": "version deleted"}


@app.delete("/documents/{doc_id}")
def delete_document(doc_id: str, db: Session = Depends(get_db)):

    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()

    db.delete(doc)
    db.commit()

    return {"message": "document deleted"}