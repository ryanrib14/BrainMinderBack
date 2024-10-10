from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, Text, ForeignKey, Integer, Enum, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.types import JSON
import enum
from uuid import uuid4

Base: DeclarativeMeta = declarative_base()

# Enum for Report Types
class ReportTypes(enum.Enum):
    TYPE1 = "TYPE1"
    TYPE2 = "TYPE2"

# Mixins for common fields
class UuidMixin:
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=uuid4(),
        index=True,
    )

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

# Domain classes
class FormattedMemory(Base, UuidMixin, TimestampMixin):
    __tablename__ = "formatted_memory"

    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    key_words: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)

    
class Document(Base, UuidMixin, TimestampMixin):
    __tablename__ = "documents"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    extension: Mapped[str] = mapped_column(Text, nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False)


class Report(Base, UuidMixin, TimestampMixin):
    __tablename__ = "reports"

    type: Mapped[ReportTypes] = mapped_column(Enum(ReportTypes), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    memory_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    key_words: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)

    def set_report(self, report_type, memories):
        # Implementar lógica de negócio aqui
        pass


class BaseChat(Base, UuidMixin, TimestampMixin):
    __tablename__ = "base_chat"

    chat: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    def validate_chat(self):
        # Implementar lógica de validação aqui
        pass

    def generate_keywords(self):
        # Implementar lógica de geração de palavras-chave aqui
        pass


class BaseMemoria(Base, UuidMixin, TimestampMixin):
    __tablename__ = "base_memoria"

    ref_chat_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("base_chat.id"), index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Optional[float]] = mapped_column(ARRAY(Integer), nullable=True)

    def generate_embedding(self):
        # Implementar lógica de geração de embedding aqui
        pass


class ChatText(BaseChat):
    __tablename__ = "chat_text"

    character_quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    def validate_chat(self):
        # Implementar lógica de validação aqui
        pass

    def generate_keywords(self):
        # Implementar lógica de geração de palavras-chave aqui
        pass


class ChatDialog(BaseChat):
    __tablename__ = "chat_dialog"

    iterations_quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    def validate_chat(self):
        # Implementar lógica de validação aqui
        pass

    def generate_keywords(self):
        # Implementar lógica de geração de palavras-chave aqui
        pass