from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
import os
import json

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class EncryptedSecret(Base):
    __tablename__ = "secrets"
    key = Column(String, primary_key=True, index=True)
    value = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

class VaultService:
    """
    Securely stores API keys and tokens using Fernet encryption.
    """
    def __init__(self):
        self.key_file = "vault.key"
        self._load_or_create_key()
        self.cipher = Fernet(self.encryption_key)

    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.encryption_key)

    def set_secret(self, key: str, value: str):
        db = SessionLocal()
        encrypted_value = self.cipher.encrypt(value.encode()).decode()
        
        existing = db.query(EncryptedSecret).filter(EncryptedSecret.key == key).first()
        if existing:
            existing.value = encrypted_value
        else:
            new_secret = EncryptedSecret(key=key, value=encrypted_value)
            db.add(new_secret)
        
        db.commit()
        db.close()

    def get_secret(self, key: str) -> str:
        db = SessionLocal()
        secret = db.query(EncryptedSecret).filter(EncryptedSecret.key == key).first()
        db.close()
        
        if secret:
            return self.cipher.decrypt(secret.value.encode()).decode()
        return None

    def list_secrets(self):
        db = SessionLocal()
        secrets = db.query(EncryptedSecret).all()
        db.close()
        return [s.key for s in secrets]

vault = VaultService()
