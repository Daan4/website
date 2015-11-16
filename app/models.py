from app import db
from flask import flash
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @classmethod
    def create(cls, success_msg=None, failure_msg=None, **kwargs):
        new_record = cls(**kwargs)
        try:
            db.session.add(new_record)
            db.session.commit()
            if success_msg:
                flash(success_msg)
        except (IntegrityError, InvalidRequestError):
            db.session.rollback()
            if failure_msg:
                flash(failure_msg)

    @classmethod
    def delete(cls, success_msg=None, unmapped_msg=None, failure_msg=None,  **kwargs):
        existing_record = cls.query.filter_by(**kwargs).first()
        try:
            db.session.delete(existing_record)
            db.session.commit()
            if success_msg:
                flash(success_msg)
        except UnmappedInstanceError:
            db.session.rollback()
            if unmapped_msg:
                flash(unmapped_msg)
        except IntegrityError:
            db.session.rollback()
            if failure_msg:
                flash(failure_msg)
