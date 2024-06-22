from dataclasses import dataclass


@dataclass
class AuthModel:
    id: int
    username: str
    password: str
    user_id: int
    created_at: str
    updated_at: str


@dataclass
class UsersModel:
    id: int
    full_name: str
    address: str
    birthday: str
    gender: str
    created_at: str
    updated_at: str
