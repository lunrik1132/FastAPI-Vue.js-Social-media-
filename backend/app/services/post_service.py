from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..repositories.post_repository import PostRepository
from ..schemas.post import PostResponse, PostListResponse, PostDeleted
from fastapi import HTTPException, status


class PostService:
    def __init__(self, db: Session):
        self.post_repository = PostRepository(db)
        self.user_repository = UserRepository(db)

    def get_all_posts(self, limit: int = 3, offset: int = 0) -> PostListResponse:
        posts = self.post_repository.get_all(limit=limit, offset=offset)

        posts_response = []
        for post, comments_count in posts:
            post.comments_count = comments_count
            posts_response.append(PostResponse.model_validate(post))

        return PostListResponse(posts=posts_response, total=len(posts_response))

    def get_post_by_id(self, post_id: int) -> PostResponse:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )

        return PostResponse.model_validate(post)

    def get_all_posts_by_author_id(
        self, author_id: int, limit: int = 3, offset: int = 0
    ) -> PostListResponse:
        user = self.user_repository.get_by_id(author_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {author_id} not found",
            )
        posts = self.post_repository.get_all_by_author_id(author_id, limit, offset)
        posts_response = []
        for post, comments_count in posts:
            post.comments_count = comments_count
            posts_response.append(PostResponse.model_validate(post))
        return PostListResponse(posts=posts_response, total=len(posts_response))

    def get_all_posts_by_destination_id(
        self, destination_id: int, limit: int = 3, offset: int = 0
    ) -> PostListResponse:
        user = self.user_repository.get_by_id(destination_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {destination_id} not found",
            )
        posts = self.post_repository.get_all_by_destination_id(
            destination_id, limit, offset
        )
        posts_response = []
        for post, comments_count in posts:
            post.comments_count = comments_count
            posts_response.append(PostResponse.model_validate(post))
        return PostListResponse(posts=posts_response, total=len(posts_response))

    def create_post(
        self, author_id: int, text: str, destination_id: int
    ) -> PostResponse:
        user = self.user_repository.get_by_id(destination_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {destination_id} not found",
            )
        post = self.post_repository.create(
            author_id=author_id, destination_id=destination_id, text=text
        )
        return PostResponse.model_validate(post)

    def delete_post_by_id(self, post_id: int, user_id: int) -> PostDeleted:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )

        if post.author_id != user_id and post.destination_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"You do not have permission to delete this post",
            )

        post = self.post_repository.delete_by_id(post_id)

        return PostDeleted.model_validate(post)

    def delete_posts_by_author_id(self, author_id: int) -> PostListResponse:
        user = self.user_repository.get_by_id(author_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {author_id} not found",
            )

        posts = self.post_repository.delete_by_author_id(author_id)
        posts_response = [PostResponse.model_validate(post) for post in posts]
        return PostListResponse(posts=posts_response, total=len(posts_response))

    def update_post_text(self, post_id: int, new_text: str) -> PostResponse:
        post = self.post_repository.update_text(post_id, new_text)
        return PostResponse.model_validate(post)
