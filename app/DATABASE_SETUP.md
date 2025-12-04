# Database Setup Guide

Complete guide for setting up the PostgreSQL database for the Maternal Health Monitoring App MVP.

## Database Schema Overview

The MVP database consists of 7 main tables:

### Core Tables

1. **users** - User authentication and basic information
   - Primary key: `user_id`
   - Stores: email, hashed_password, full_name, platform_token, timestamps

2. **pregnancy_profiles** - Pregnancy-specific data (One-to-One with users)
   - Primary key: `profile_id`
   - Foreign key: `user_id` → `users.user_id`
   - Stores: EDD, LMP, initial_weight_kg, calculated pregnancy week

3. **symptom_logs** - Daily symptom, mood, and journal entries
   - Primary key: `log_id`
   - Foreign key: `user_id` → `users.user_id`
   - Stores: symptom_type (ENUM), severity_rating (1-5), mood (ENUM), journal_entry

4. **weight_logs** - Daily weight tracking
   - Primary key: `weight_log_id`
   - Foreign key: `user_id` → `users.user_id`
   - Stores: weight_kg, log_date, pregnancy_week

### Static Content Tables

5. **weekly_content** - Educational content for weeks 1-12
   - Primary key: `content_id`
   - Unique: `week_number` (1-12 for MVP)
   - Stores: title, focus, body

6. **visit_explanations** - Prenatal visit guidance (Visits 1-4)
   - Primary key: `visit_id`
   - Unique: `visit_number` (1-4 for MVP)
   - Stores: title, purpose, what_happens, typical_week

### Feedback Table

7. **feedbacks** - User satisfaction (NPS) feedback
   - Primary key: `feedback_id`
   - Foreign key: `user_id` → `users.user_id`
   - Stores: nps_score (0-10), feedback_text, pregnancy_week

## Prerequisites

- PostgreSQL 12 or higher
- Python 3.9+
- Virtual environment activated

## Step 1: Install PostgreSQL

### macOS (using Homebrew)
```bash
brew install postgresql@15
brew services start postgresql@15
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Windows
Download and install from [PostgreSQL Official Website](https://www.postgresql.org/download/windows/)

## Step 2: Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE maternal_health_db;

# Create user (optional, for security)
CREATE USER maternal_app_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE maternal_health_db TO maternal_app_user;

# Exit psql
\q
```

## Step 3: Configure Environment Variables

Update your `.env` file:

```bash
DATABASE_URL=postgresql://maternal_app_user:your_secure_password@localhost:5432/maternal_health_db
```

## Step 4: Install Python Dependencies

Ensure all database-related packages are installed:

```bash
pip install sqlalchemy psycopg2-binary alembic python-dotenv
```

## Step 5: Initialize Alembic

Alembic is already configured in the project. Verify the setup:

```bash
# Check alembic.ini exists
ls -la alembic.ini

# Check migrations directory
ls -la alembic/versions/
```

## Step 6: Run Migrations

Apply the initial schema migration:

```bash
# Run the migration
alembic upgrade head

# Verify tables were created
psql -U maternal_app_user -d maternal_health_db -c "\dt"
```

Expected output:
```
                List of relations
 Schema |        Name          | Type  |      Owner
--------+----------------------+-------+-----------------
 public | alembic_version      | table | maternal_app_user
 public | feedbacks            | table | maternal_app_user
 public | pregnancy_profiles   | table | maternal_app_user
 public | symptom_logs         | table | maternal_app_user
 public | users                | table | maternal_app_user
 public | visit_explanations   | table | maternal_app_user
 public | weekly_content       | table | maternal_app_user
 public | weight_logs          | table | maternal_app_user
```

## Step 7: Seed Static Content

Populate the weekly_content and visit_explanations tables:

```bash
python scripts/seed_content.py
```

Expected output:
```
============================================================
Maternal Health Monitoring App - Content Seeding Script
============================================================

Seeding weekly content...
  ✓ Added Week 1: Week 1 & 2: Preparing for the Journey
  ✓ Added Week 2: Week 1 & 2: Preparing for the Journey
  ✓ Added Week 3: Week 3: Tiny Beginnings
  ...
  ✓ Added Week 12: Week 12: Officially Finishing the First Trimester!
Weekly content seeding complete!

Seeding visit explanations...
  ✓ Added Visit 1: Visit 1 (Around 8 Weeks): The Confirmation & Plan
  ✓ Added Visit 2: Visit 2 (Around 12 Weeks): First Trimester Checkpoint
  ✓ Added Visit 3: Visit 3 (Around 16 Weeks): Early Second Trimester Check-in
  ✓ Added Visit 4: Visit 4 (Around 20 Weeks): Anatomy Scan Review
Visit explanations seeding complete!

============================================================
✓ All content seeded successfully!
============================================================
```

## Step 8: Verify Database Setup

Check that everything is working:

```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Test the health check endpoint
curl http://localhost:8000/health
```

## Database Management Commands

### View Current Migration Status
```bash
alembic current
```

### Create a New Migration (after model changes)
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Rollback Migration
```bash
alembic downgrade -1  # Rollback one version
alembic downgrade base  # Rollback all migrations
```

### Reset Database (Development Only)
```bash
# Drop all tables
alembic downgrade base

# Recreate tables
alembic upgrade head

# Re-seed content
python scripts/seed_content.py
```

## Database Queries for Testing

### Check User Count
```sql
SELECT COUNT(*) FROM users;
```

### View Weekly Content
```sql
SELECT week_number, title FROM weekly_content ORDER BY week_number;
```

### View Visit Explanations
```sql
SELECT visit_number, title, typical_week FROM visit_explanations ORDER BY visit_number;
```

### Check Recent Logs for a User
```sql
SELECT u.email, sl.log_date, sl.symptom_type, sl.mood 
FROM symptom_logs sl
JOIN users u ON sl.user_id = u.user_id
ORDER BY sl.log_date DESC
LIMIT 10;
```

## Entity Relationship Diagram (Text Format)

```
users (1) ←→ (1) pregnancy_profiles
  ↓
  (1:N) symptom_logs
  (1:N) weight_logs
  (1:N) feedbacks

weekly_content (standalone, weeks 1-12)
visit_explanations (standalone, visits 1-4)
```

## ENUM Types

### SymptomType
- NAUSEA
- FATIGUE
- HEADACHE
- BREAST_TENDERNESS
- CRAMPING
- BLOATING
- FOOD_AVERSION
- FREQUENT_URINATION
- SPOTTING
- MOOD_SWINGS

### MoodType
- HAPPY
- ANXIOUS
- TIRED
- IRRITABLE
- EXCITED
- CALM
- OVERWHELMED
- NEUTRAL

## Troubleshooting

### Issue: "relation does not exist"
**Solution:** Run migrations
```bash
alembic upgrade head
```

### Issue: "could not connect to server"
**Solution:** Ensure PostgreSQL is running
```bash
# macOS
brew services restart postgresql@15

# Ubuntu/Debian
sudo systemctl restart postgresql
```

### Issue: "password authentication failed"
**Solution:** Check your DATABASE_URL in `.env` file

### Issue: "peer authentication failed"
**Solution:** Edit PostgreSQL's `pg_hba.conf` to use `md5` instead of `peer` for local connections

## Security Best Practices

1. **Never commit `.env` file** - Contains database credentials
2. **Use strong passwords** - For database users
3. **Limit database user privileges** - In production, only grant necessary permissions
4. **Enable SSL** - For production database connections
5. **Regular backups** - Set up automated database backups
6. **Encrypt sensitive data** - Consider encrypting health data at rest

## Production Considerations

For production deployment:

1. Use managed PostgreSQL service (AWS RDS, Google Cloud SQL, Azure Database)
2. Enable connection pooling (already configured in `database.py`)
3. Set up read replicas for scaling
4. Configure automated backups
5. Enable monitoring and alerting
6. Use connection SSL/TLS
7. Implement database migration strategy (blue-green deployments)

## Next Steps

After database setup:

1. Implement authentication endpoints (`/v1/auth/register`)
2. Create user profile endpoints (`/v1/users/profile`)
3. Build daily logging endpoints (`/v1/logs/daily`)
4. Implement content delivery endpoints (`/v1/content/week/{week_number}`)

## Support

For database-related issues, contact the backend development team.