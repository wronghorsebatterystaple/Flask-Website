from flask import current_app
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.types import Text
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timezone
import re
from typing import Optional

from app import db
from app import login_manager
from app.db_config import db_config


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    blog_id: so.Mapped[int] = so.mapped_column(index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
            index=True, default=lambda: datetime.now(timezone.utc))
    edited_timestamp: so.Mapped[datetime] = so.mapped_column(nullable=True, default=None)
    title: so.Mapped[str] = so.mapped_column(sa.String(db_config["MAXLEN_POST_TITLE"]),
            unique=True)
    sanitized_title: so.Mapped[str] = so.mapped_column(sa.String(db_config["MAXLEN_POST_TITLE"]),
            unique=True)
    subtitle: so.Mapped[str] = so.mapped_column(sa.String(db_config["MAXLEN_POST_SUBTITLE"]),
            nullable=True, default=None)
    content: so.Mapped[Text()] = so.mapped_column(Text(db_config["MAXLEN_POST_CONTENT"]))

    comments: so.WriteOnlyMapped["Comment"] = so.relationship(back_populates="post",
            cascade="all, delete, delete-orphan", passive_deletes=True)

    def sanitize_title(self):
        self.sanitized_title = ("-".join(self.title.split())).lower()
        self.sanitized_title = re.sub("[^A-Za-z0-9-]", "", self.sanitized_title)

    def expand_image_markdown(self):
        self.content = re.sub(r"(!\[[\S\s]*?\])\(([\S\s]+?)\)",
                fr"\1({current_app.config['BLOGPAGE_STATIC_FROM_ROUTES']}/{self.blog_id}/images/{self.id}/\2)", self.content)

    def collapse_image_markdown(self) -> str:
        return re.sub(fr"(!\[[\S\s]*?\])\({current_app.config['BLOGPAGE_STATIC_FROM_ROUTES']}/{self.blog_id}/images/{self.id}/([\S\s]+?)\)",
                r"\1(\2)", self.content)

    def are_titles_unique(self) -> bool:
        return db.session.query(Post).filter_by(sanitized_title = self.sanitized_title).first() is None

    def __repr__(self):
        return f"<Post {self.id} with title \"{self.title}\" and subtitle \"{self.subtitle}\">"


class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id, ondelete="CASCADE"))
    timestamp: so.Mapped[datetime] = so.mapped_column(
            index=True, default=lambda: datetime.now(timezone.utc))
    author: so.Mapped[str] = so.mapped_column(sa.String(db_config["MAXLEN_COMMENT_AUTHOR"]))
    content: so.Mapped[Text()] = so.mapped_column(Text(db_config["MAXLEN_COMMENT_CONTENT"]))

    post: so.Mapped[Post] = so.relationship(back_populates="comments")

    # nested set; quite the beautiful data structure
    left: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    right: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    depth: so.Mapped[int] = so.mapped_column(sa.Integer)

    def insert_comment(self, post, parent) -> bool:
        if parent is None: # add child with left = max of right for that post + 1
            max_right_query = post.comments.select().order_by(sa.desc(Comment.right)).limit(1)
            max_right_comment = db.session.scalars(max_right_query).first()
            max_right = 0
            if max_right_comment is not None:
                max_right = max_right_comment.right
            self.left = max_right + 1
            self.right = max_right + 2
            self.depth = 0
            return True

        if self.post_id != parent.post_id or self.post_id != post.id: # sanity check
            return False

        self.left = parent.right
        self.right = parent.right + 1
        self.depth = parent.depth + 1

        comments_to_update_query = post.comments.select().filter(Comment.right >= parent.right)
        comments_to_update = db.session.scalars(comments_to_update_query).all()
        for comment in comments_to_update:
            if comment.left >= parent.right:
                comment.left += 2
            comment.right += 2
        return True

    def get_descendants_list(self, post) -> list:
        comments_query = post.comments.select().filter(sa.and_(
                Comment.left > self.left, Comment.right < self.right))
        return db.session.scalars(comments_query).all()

    def __repr(self):
        return f"<Comment {self.id} for post {self.post_id} written by \"{self.author}\""


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(db_config["MAXLEN_USER_USERNAME"]),
            unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(db_config["MAXLEN_USER_EMAIL"]),
            unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(db_config["MAXLEN_USER_PASSWORD_HASH"]))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
	return db.session.get(User, int(id))
