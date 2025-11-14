import pytest
from models.user import User
from services.user_service import UserService

class DummyRequest:
    def __init__(self, username, password, role="USER"):
        self.username = username
        self.password = password
        self.role = role

def test_register_user_existing():
    class DummyDB:
        def query(self, model):
            class Q:
                def filter(self, *args, **kwargs):
                    return self
                def first(self):
                    return User(username="test", hashed_password="hashed", role="USER")
            return Q()
        def close(self): pass
    req = DummyRequest("test", "password")
    result = UserService.register_user(req, DummyDB())
    assert "error" in result

def test_register_user_success():
    class DummyDB:
        def query(self, model):
            class Q:
                def filter(self, *args, **kwargs):
                    return self
                def first(self):
                    return None
            return Q()
        def add(self, user): pass
        def commit(self): pass
        def refresh(self, user): pass
        def close(self): pass
    req = DummyRequest("newuser", "password")
    result = UserService.register_user(req, DummyDB())
    assert result["msg"] == "User registered"
