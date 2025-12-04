"""
Database Models for Maternal Health Monitoring App MVP
SQLAlchemy ORM Models based on System Architecture Document
"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class User(Base):
    """
    User table - Stores user authentication and basic information
    Managed by Auth Service & Backend
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    
    # Push notification token for daily check-in reminders (Feature 4)
    platform_token = Column(String(512), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Account status
    is_active = Column(Integer, default=1, nullable=False)  # 1 = active, 0 = inactive
    
    # Relationships
    pregnancy_profile = relationship("PregnancyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    symptom_logs = relationship("SymptomLog", back_populates="user", cascade="all, delete-orphan")
    weight_logs = relationship("WeightLog", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email})>"


class PregnancyProfile(Base):
    """
    PregnancyProfile table - One-to-One with User
    Stores pregnancy-specific information (Feature 2, 3)
    AC 2.1: System calculates current week based on EDD/LMP
    AC 3.1: Changing EDD recalculates all future content
    """
    __tablename__ = "pregnancy_profiles"

    profile_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    # Pregnancy dates (Feature 2)
    edd = Column(Date, nullable=True, comment="Estimated Due Date")
    lmp_start_date = Column(Date, nullable=True, comment="Last Menstrual Period start date - used for calculation if EDD is missing")
    
    # Initial weight at profile setup (Feature 3)
    initial_weight_kg = Column(Float, nullable=True, comment="Initial weight in kilograms")
    
    # Calculated fields (cached for performance)
    current_week = Column(Integer, nullable=True, comment="Cached current week of pregnancy")
    current_day = Column(Integer, nullable=True, comment="Cached current day within the week")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="pregnancy_profile")

    def __repr__(self):
        return f"<PregnancyProfile(profile_id={self.profile_id}, user_id={self.user_id}, edd={self.edd})>"


class MoodType(enum.Enum):
    """Enum for mood types (AC 7.1: predefined, non-judgmental terms)"""
    HAPPY = "Happy"
    ANXIOUS = "Anxious"
    TIRED = "Tired"
    IRRITABLE = "Irritable"
    EXCITED = "Excited"
    CALM = "Calm"
    OVERWHELMED = "Overwhelmed"
    NEUTRAL = "Neutral"


class SymptomType(enum.Enum):
    """Enum for common first-trimester symptoms"""
    NAUSEA = "Nausea"
    FATIGUE = "Fatigue"
    HEADACHE = "Headache"
    BREAST_TENDERNESS = "Breast Tenderness"
    CRAMPING = "Cramping"
    BLOATING = "Bloating"
    FOOD_AVERSION = "Food Aversion"
    FREQUENT_URINATION = "Frequent Urination"
    SPOTTING = "Spotting"
    MOOD_SWINGS = "Mood Swings"


class SymptomLog(Base):
    """
    SymptomLog table - Tracks daily symptoms, mood, and journal entries
    Features 5, 7, 8 (Daily Check-in & Logging)
    AC 5.1: Symptom selection via friendly icons
    AC 7.1: Mood uses simple scale or predefined terms
    AC 8.1: Optional free-form journaling
    """
    __tablename__ = "symptom_logs"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Log date (indexed for querying trends)
    log_date = Column(Date, nullable=False, index=True, default=date.today)
    
    # Symptom tracking (Feature 5)
    symptom_type = Column(SQLEnum(SymptomType), nullable=True, comment="Type of symptom experienced")
    severity_rating = Column(Integer, nullable=True, comment="Severity rating 1-5 (AC 5.1)")
    
    # Mood tracking (Feature 7 - AC 7.1)
    mood = Column(SQLEnum(MoodType), nullable=True, comment="Daily mood selection")
    
    # Free-form journaling (Feature 8 - AC 8.1)
    journal_entry = Column(Text, nullable=True, comment="Optional daily journal text")
    
    # Pregnancy week at time of log (for trend analysis)
    pregnancy_week = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="symptom_logs")

    def __repr__(self):
        return f"<SymptomLog(log_id={self.log_id}, user_id={self.user_id}, date={self.log_date})>"


class WeightLog(Base):
    """
    WeightLog table - Tracks daily weight entries
    Feature 6 (Weight Logging)
    AC 6.1: Display last recorded weight upon entry
    AC 12.1: Weight Trend Chart displays last 7 and 30 days
    """
    __tablename__ = "weight_logs"

    weight_log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Log date (indexed for trend queries)
    log_date = Column(Date, nullable=False, index=True, default=date.today)
    
    # Weight (stored in KG, converted to LBS on frontend if needed)
    weight_kg = Column(Float, nullable=False, comment="Weight in kilograms")
    
    # Pregnancy week at time of log
    pregnancy_week = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="weight_logs")

    def __repr__(self):
        return f"<WeightLog(weight_log_id={self.weight_log_id}, user_id={self.user_id}, weight={self.weight_kg}kg)>"


class WeeklyContent(Base):
    """
    WeeklyContent table - Static, curated educational content for weeks 1-12
    Feature 9 (Week-Specific Content Access)
    AC 9.1: Users cannot access content beyond their current week
    Content limited to Weeks 1-12 (Out-of-Scope constraint)
    """
    __tablename__ = "weekly_content"

    content_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Week number (1-12 only for MVP)
    week_number = Column(Integer, unique=True, nullable=False, index=True, comment="Pregnancy week (1-12 for MVP)")
    
    # Content fields
    title = Column(String(255), nullable=False, comment="Week title (e.g., 'Week 8: The Heartbeat Milestone')")
    focus = Column(String(500), nullable=True, comment="Main focus of the week")
    body = Column(Text, nullable=False, comment="Detailed educational content")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<WeeklyContent(content_id={self.content_id}, week={self.week_number}, title={self.title})>"


class VisitExplanation(Base):
    """
    VisitExplanation table - Static content for prenatal visit expectations
    Corresponds to the 4 early pregnancy visits guide
    Helps reduce anxiety by explaining what to expect at each appointment
    """
    __tablename__ = "visit_explanations"

    visit_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Visit details
    visit_number = Column(Integer, unique=True, nullable=False, index=True, comment="Visit number (1-4 for MVP)")
    typical_week = Column(Integer, nullable=False, comment="Typical week this visit occurs (e.g., 8, 12, 16, 20)")
    
    # Content fields
    title = Column(String(255), nullable=False, comment="Visit title (e.g., 'Visit 1: The Confirmation & Plan')")
    purpose = Column(Text, nullable=False, comment="Purpose of the visit")
    what_happens = Column(Text, nullable=False, comment="What happens during the visit")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<VisitExplanation(visit_id={self.visit_id}, visit_number={self.visit_number}, title={self.title})>"


class Feedback(Base):
    """
    Feedback table - Stores user satisfaction feedback (NPS)
    Feature 15 (User Satisfaction Feedback)
    AC 15.1: NPS prompt is non-intrusive and can be dismissed/deferred
    """
    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # NPS Rating (0-10)
    nps_score = Column(Integer, nullable=False, comment="Net Promoter Score (0-10)")
    
    # Optional feedback text
    feedback_text = Column(Text, nullable=True, comment="Optional user feedback")
    
    # Pregnancy week when feedback was given
    pregnancy_week = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="feedbacks")

    def __repr__(self):
        return f"<Feedback(feedback_id={self.feedback_id}, user_id={self.user_id}, nps={self.nps_score})>"