from sqlalchemy.orm import Session
from .models import Document, DocumentVersion
from datetime import datetime

def create_document(db: Session, title, content, user):

    doc = Document(
        title=title,
        created_by=user
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    version = DocumentVersion(
        document_id=doc.id,
        content=content,
        version_number=1,
        modified_by=user
    )

    db.add(version)
    db.commit()

    return doc


def get_latest_version(db, doc_id):

    return db.query(DocumentVersion)\
        .filter(DocumentVersion.document_id == doc_id)\
        .order_by(DocumentVersion.version_number.desc())\
        .first()