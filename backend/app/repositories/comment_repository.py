from sqlalchemy.orm import Session, joinedload
from ..models.comment import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_post_id(
        self, post_id: int, limit: int = 3, offset: int = 1
    ) -> list[Comment]:
        db_comments = (
            self.db.query(Comment)
            .options(joinedload(Comment.author))
            .filter(Comment.post_id == post_id)
            .order_by(Comment.date_created)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return db_comments

    def get_by_id(self, comment_id: int) -> Comment:
        db_comment = (
            self.db.query(Comment)
            .options(joinedload(Comment.author))
            .filter(Comment.id == comment_id)
            .first()
        )
        return db_comment

    def add(self, post_id: int, text: str, author_id: int) -> Comment:
        db_comment = Comment(post_id=post_id, author_id=author_id, text=text)
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def delete_by_comment_id(self, comment_id: int) -> Comment:
        db_comment = (
            self.db.query(Comment)
            .options(joinedload(Comment.author))
            .filter(Comment.id == comment_id)
            .first()
        )

        self.db.delete(db_comment)
        self.db.commit()
        return db_comment
