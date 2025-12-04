"""Initial schema for Maternal Health Monitoring App MVP

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-12-04 10:00:00.000000

Creates tables for:
- users: User authentication and basic info
- pregnancy_profiles: Pregnancy-specific data (EDD, LMP, initial weight)
- symptom_logs: Daily symptom, mood, and journal entries
- weight_logs: Daily weight tracking
- weekly_content: Educational content for weeks 1-12
- visit_explanations: Prenatal visit guidance
- feedbacks: User satisfaction (NPS) feedback
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Create all tables for MVP v1.0
    """
    
    # Create ENUM types for PostgreSQL
    symptom_type_enum = postgresql.ENUM(
        'NAUSEA', 'FATIGUE', 'HEADACHE', 'BREAST_TENDERNESS', 
        'CRAMPING', 'BLOATING', 'FOOD_AVERSION', 'FREQUENT_URINATION',
        'SPOTTING', 'MOOD_SWINGS',
        name='symptomtype',
        create_type=True
    )
    
    mood_type_enum = postgresql.ENUM(
        'HAPPY', 'ANXIOUS', 'TIRED', 'IRRITABLE', 
        'EXCITED', 'CALM', 'OVERWHELMED', 'NEUTRAL',
        name='moodtype',
        create_type=True
    )
    
    symptom_type_enum.create(op.get_bind(), checkfirst=True)
    mood_type_enum.create(op.get_bind(), checkfirst=True)
    
    # 1. Create users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('platform_token', sa.String(length=512), nullable=True, comment='Push notification token'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1'),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # 2. Create pregnancy_profiles table (One-to-One with users)
    op.create_table(
        'pregnancy_profiles',
        sa.Column('profile_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('edd', sa.Date(), nullable=True, comment='Estimated Due Date'),
        sa.Column('lmp_start_date', sa.Date(), nullable=True, comment='Last Menstrual Period start date'),
        sa.Column('initial_weight_kg', sa.Float(), nullable=True, comment='Initial weight in kilograms'),
        sa.Column('current_week', sa.Integer(), nullable=True, comment='Cached current week of pregnancy'),
        sa.Column('current_day', sa.Integer(), nullable=True, comment='Cached current day within the week'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('profile_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_pregnancy_profiles_profile_id'), 'pregnancy_profiles', ['profile_id'], unique=False)
    op.create_index(op.f('ix_pregnancy_profiles_user_id'), 'pregnancy_profiles', ['user_id'], unique=True)
    
    # 3. Create symptom_logs table
    op.create_table(
        'symptom_logs',
        sa.Column('log_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('log_date', sa.Date(), nullable=False),
        sa.Column('symptom_type', symptom_type_enum, nullable=True, comment='Type of symptom experienced'),
        sa.Column('severity_rating', sa.Integer(), nullable=True, comment='Severity rating 1-5'),
        sa.Column('mood', mood_type_enum, nullable=True, comment='Daily mood selection'),
        sa.Column('journal_entry', sa.Text(), nullable=True, comment='Optional daily journal text'),
        sa.Column('pregnancy_week', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('log_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_symptom_logs_log_id'), 'symptom_logs', ['log_id'], unique=False)
    op.create_index(op.f('ix_symptom_logs_user_id'), 'symptom_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_symptom_logs_log_date'), 'symptom_logs', ['log_date'], unique=False)
    
    # 4. Create weight_logs table
    op.create_table(
        'weight_logs',
        sa.Column('weight_log_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('log_date', sa.Date(), nullable=False),
        sa.Column('weight_kg', sa.Float(), nullable=False, comment='Weight in kilograms'),
        sa.Column('pregnancy_week', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('weight_log_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_weight_logs_weight_log_id'), 'weight_logs', ['weight_log_id'], unique=False)
    op.create_index(op.f('ix_weight_logs_user_id'), 'weight_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_weight_logs_log_date'), 'weight_logs', ['log_date'], unique=False)
    
    # 5. Create weekly_content table (Static content for weeks 1-12)
    op.create_table(
        'weekly_content',
        sa.Column('content_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('week_number', sa.Integer(), nullable=False, comment='Pregnancy week (1-12 for MVP)'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('focus', sa.String(length=500), nullable=True),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('content_id'),
        sa.UniqueConstraint('week_number')
    )
    op.create_index(op.f('ix_weekly_content_content_id'), 'weekly_content', ['content_id'], unique=False)
    op.create_index(op.f('ix_weekly_content_week_number'), 'weekly_content', ['week_number'], unique=True)
    
    # 6. Create visit_explanations table
    op.create_table(
        'visit_explanations',
        sa.Column('visit_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('visit_number', sa.Integer(), nullable=False, comment='Visit number (1-4 for MVP)'),
        sa.Column('typical_week', sa.Integer(), nullable=False, comment='Typical week this visit occurs'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('purpose', sa.Text(), nullable=False),
        sa.Column('what_happens', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('visit_id'),
        sa.UniqueConstraint('visit_number')
    )
    op.create_index(op.f('ix_visit_explanations_visit_id'), 'visit_explanations', ['visit_id'], unique=False)
    op.create_index(op.f('ix_visit_explanations_visit_number'), 'visit_explanations', ['visit_number'], unique=True)
    
    # 7. Create feedbacks table
    op.create_table(
        'feedbacks',
        sa.Column('feedback_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('nps_score', sa.Integer(), nullable=False, comment='Net Promoter Score (0-10)'),
        sa.Column('feedback_text', sa.Text(), nullable=True, comment='Optional user feedback'),
        sa.Column('pregnancy_week', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('feedback_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_feedbacks_feedback_id'), 'feedbacks', ['feedback_id'], unique=False)
    op.create_index(op.f('ix_feedbacks_user_id'), 'feedbacks', ['user_id'], unique=False)


def downgrade():
    """
    Drop all tables in reverse order
    """
    
    # Drop tables
    op.drop_index(op.f('ix_feedbacks_user_id'), table_name='feedbacks')
    op.drop_index(op.f('ix_feedbacks_feedback_id'), table_name='feedbacks')
    op.drop_table('feedbacks')
    
    op.drop_index(op.f('ix_visit_explanations_visit_number'), table_name='visit_explanations')
    op.drop_index(op.f('ix_visit_explanations_visit_id'), table_name='visit_explanations')
    op.drop_table('visit_explanations')
    
    op.drop_index(op.f('ix_weekly_content_week_number'), table_name='weekly_content')
    op.drop_index(op.f('ix_weekly_content_content_id'), table_name='weekly_content')
    op.drop_table('weekly_content')
    
    op.drop_index(op.f('ix_weight_logs_log_date'), table_name='weight_logs')
    op.drop_index(op.f('ix_weight_logs_user_id'), table_name='weight_logs')
    op.drop_index(op.f('ix_weight_logs_weight_log_id'), table_name='weight_logs')
    op.drop_table('weight_logs')
    
    op.drop_index(op.f('ix_symptom_logs_log_date'), table_name='symptom_logs')
    op.drop_index(op.f('ix_symptom_logs_user_id'), table_name='symptom_logs')
    op.drop_index(op.f('ix_symptom_logs_log_id'), table_name='symptom_logs')
    op.drop_table('symptom_logs')
    
    op.drop_index(op.f('ix_pregnancy_profiles_user_id'), table_name='pregnancy_profiles')
    op.drop_index(op.f('ix_pregnancy_profiles_profile_id'), table_name='pregnancy_profiles')
    op.drop_table('pregnancy_profiles')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
    
    # Drop ENUM types
    sa.Enum(name='moodtype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='symptomtype').drop(op.get_bind(), checkfirst=True)