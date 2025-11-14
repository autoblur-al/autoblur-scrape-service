import logging
from models.user import User
from db.database import SessionLocal
from services.auth_service import hash_password, verify_password
from services.jwt_service import create_access_token

logger = logging.getLogger("autoblur.user_service")

class UserService:
    @staticmethod
    def register_user(request, db):
        logger.debug(f"Received registration request: username={request.username}, role={request.role}")
        if len(request.password.encode('utf-8')) > 72:
            logger.info(f"Registration failed: Password too long (bytes) for username '{request.username}'.")
            return {"error": "Password cannot be longer than 72 bytes (ASCII or UTF-8)."}
        try:
            if db.query(User).filter(User.username == request.username).first():
                logger.info(f"Registration failed: Username '{request.username}' already exists.")
                return {"error": "Username already exists"}
            hashed_pw = hash_password(request.password)
            user = User(username=request.username, hashed_password=hashed_pw, role=request.role)
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"User '{request.username}' registered successfully.")
            return {"msg": "User registered"}
        except Exception as e:
            logger.error(f"Registration error: {e}", exc_info=True)
            return {"error": "Internal Server Error"}

    @staticmethod
    def login_user(request, db):
        logger.debug(f"Received login request: username={request.username}")
        try:
            user = db.query(User).filter(User.username == request.username).first()
            if not user or not verify_password(request.password, user.hashed_password):
                logger.info(f"Login failed for username={request.username}")
                return {"error": "Invalid credentials"}
            token = create_access_token({"sub": user.username, "role": user.role})
            logger.info(f"Login successful for username={request.username}")
            return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            logger.error(f"Login error: {e}", exc_info=True)
            return {"error": "Internal Server Error"}
