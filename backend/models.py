from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import CreateDomainType
from enum import StrEnum
import sqlalchemy as sa 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, DateTime,Enum as SQLEnum

class DebateStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class PersonaType(StrEnum):
    OPTIMIST = "optimist"
    REALIST = "realist"
    SKEPTIC = "skeptic"

class base(DeclarativeBase):
    pass
class Debate(base):
    __tablename__ = "DEBATE"
    id=Column(Integer, primary_key=True, index = True)
    topic = Column(String, nullable = False)
    rounds_count = Column(Integer, default=5,nullable=False)
    status = Column(SQLEnum(DebateStatus),default = DebateStatus.PENDING,nullable=False)
    consensus_score = Column(Float,default=0.0, nullable = False)
    winner = Column(String, nullable = True)
    created_at = Column(DateTime, default = sa.func.now(), nullable=False)
    user_analogy = Column(Text, nullable = False)
class DebateAgent(base):
    __tablename__ = "DEBATEAGENT"
    id=Column(Integer,primary_key=True,index=True)
    debate_id=Column(Integer,ForeignKey("debate_id"), nullable = False)
    name = Column(String)
    persona = Column(SQLEnum(PersonaType()))
    final_position = Column(Text, nullable=True)
    model_name = Column(String)

class Argument(base):
    id = Column(Integer, primary_key=True, nullable=False)
    debate_id = Column(Integer, ForeignKey("DEBATE.id"))
    agent_id = Column(Integer,ForeignKey("DEBATEAGENT.id"))
    round_number=Column(Integer)
    content = Column(Text)
    quality_score = Column(Float)
    consensus_contribution = Column(Float)
    created_at = Column(DateTime,timezone = True)
    persuasiveness_score = Column(Float)

class RoundSummary(base):
    id = Column(Integer, primary_key=True)
    debate_id = Column(Integer, ForeignKey("Debates.id"))
    round_number = Column(Integer)
    consensus_score = Column(Float)
    summary = Column(Text)

