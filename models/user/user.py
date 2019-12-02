from uuid import uuid4
from dataclasses import dataclass, field
from typing import Dict
from models.model import Model
from common.utils import Utils
import models.user.errors as UserErrors


@dataclass
class User(Model):
    collection: str = field(init=False, default="users")
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by("email", email)
        except TypeError:
            raise UserErrors.UserNotFoundError("No user found with this email.")

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email entered does not have the right format.")

        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError("The email entered was already used.")
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        user = cls.find_by_email(email)

        if not Utils.check_hashed_password(password, user.password):
            raise UserErrors.IncorrectPasswordError("The entered password is incorrect")

        return True

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }
