"""Database models matching existing Drizzle schema"""

import uuid
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Lottery(Base):
    """Lottery table - matches existing Drizzle schema"""
    __tablename__ = "lottery"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    slug = Column(Text, nullable=False, unique=True, index=True)
    country = Column(Text, nullable=False)
    region = Column(Text)
    frequency = Column(Text)  # e.g., "Mon, Thu"
    logo = Column(Text)
    description = Column(Text)
    officialLink = Column("officialLink", Text)  # Maps to source URL
    isActive = Column("isActive", Boolean, default=True)
    createdAt = Column("createdAt", DateTime, server_default=func.now())
    updatedAt = Column("updatedAt", DateTime, server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Lottery {self.slug}: {self.name}>"


class Result(Base):
    """Result table - matches existing Drizzle schema"""
    __tablename__ = "result"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lotteryId = Column("lotteryId", UUID(as_uuid=True), ForeignKey("lottery.id"), nullable=False)
    drawDate = Column("drawDate", DateTime, nullable=False)
    numbers = Column(JSON, nullable=False)  # {"main": [1,2,3], "bonus": [4]}
    jackpot = Column(Text)  # e.g., "€100M"
    currency = Column(Text, default="EUR")
    winners = Column(JSON)  # [{"tier": 1, "prize": 1000000, "count": 1}]
    createdAt = Column("createdAt", DateTime, server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Result lottery_id={self.lotteryId} date={self.drawDate}>"


class ScraperJob(Base):
    """Scraper job execution tracking"""
    __tablename__ = "scraper_job"
    
    id = Column(Integer, primary_key=True)
    lotteryId = Column("lotteryId", UUID(as_uuid=True), ForeignKey("lottery.id"), nullable=False)
    status = Column(String(20), nullable=False)  # pending, running, success, failed
    startedAt = Column("startedAt", DateTime)
    completedAt = Column("completedAt", DateTime)
    errorMessage = Column("errorMessage", Text)
    resultsCount = Column("resultsCount", Integer, default=0)
    executionTimeMs = Column("executionTimeMs", Integer)
    createdAt = Column("createdAt", DateTime, server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<ScraperJob {self.id}: {self.status}>"


class ScraperConfig(Base):
    """Scraper configuration"""
    __tablename__ = "scraper_config"
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(JSON, nullable=False)
    description = Column(Text)
    updatedAt = Column("updatedAt", DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<ScraperConfig {self.key}>"
