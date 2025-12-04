"""
Seed Script for Static Content
Populates weekly_content and visit_explanations tables with MVP content
Based on the content documents provided
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, engine
from app.db.models import WeeklyContent, VisitExplanation, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Weekly content data (Weeks 1-12)
WEEKLY_CONTENT_DATA = [
    {
        "week_number": 1,
        "title": "Week 1 & 2: Preparing for the Journey",
        "focus": "These weeks technically cover pre-conception or early menstruation before ovulation, but we start here to align with the clinical 40-week count.",
        "body": "You are officially at the beginning of this incredible journey! While you might not feel different yet, your body is busy preparing the perfect environment. Keep taking care of yourself—the healthiest version of you is the best foundation for what's to come."
    },
    {
        "week_number": 2,
        "title": "Week 1 & 2: Preparing for the Journey",
        "focus": "These weeks technically cover pre-conception or early menstruation before ovulation, but we start here to align with the clinical 40-week count.",
        "body": "You are officially at the beginning of this incredible journey! While you might not feel different yet, your body is busy preparing the perfect environment. Keep taking care of yourself—the healthiest version of you is the best foundation for what's to come."
    },
    {
        "week_number": 3,
        "title": "Week 3: Tiny Beginnings",
        "focus": "Implantation and early hormonal changes.",
        "body": "A monumental event is taking place this week: your baby (still a tiny ball of cells!) is settling in. You may notice some light spotting or cramping—it's often just the sign of implantation, which is completely normal and a positive step in your pregnancy."
    },
    {
        "week_number": 4,
        "title": "Week 4: The Hormones Arrive",
        "focus": "The week a period is typically missed; first signs of symptoms.",
        "body": "This is likely the week you find out you're pregnant! The rapid rise in pregnancy hormones is starting, which may bring on some mild fatigue or soreness. Give yourself permission to slow down and rest whenever your body asks for it."
    },
    {
        "week_number": 5,
        "title": "Week 5: Hello, Fatigue!",
        "focus": "Fatigue becomes a major symptom; the embryo is growing rapidly.",
        "body": "The fatigue this week can feel overwhelming, but it's a direct sign that your body is working incredibly hard building the life support system for your baby. Remember that feeling exhausted is common and completely normal in the early weeks."
    },
    {
        "week_number": 6,
        "title": "Week 6: Nausea Peaks",
        "focus": "Morning sickness/nausea may intensify.",
        "body": "If you're feeling nauseous (or 'morning sick'—which can happen anytime!), try small, frequent snacks to keep your stomach settled. This symptom is often viewed as a positive sign of those vital pregnancy hormones doing their job perfectly."
    },
    {
        "week_number": 7,
        "title": "Week 7: Building Connections",
        "focus": "Organ development begins; continued discomfort.",
        "body": "Your baby is now forming their core internal organs! Meanwhile, you might notice increased trips to the bathroom due to hormonal changes and increased blood flow. This is a typical, temporary inconvenience—stay hydrated and be patient with your body."
    },
    {
        "week_number": 8,
        "title": "Week 8: The Heartbeat Milestone",
        "focus": "Often the first prenatal appointment; hearing the heartbeat.",
        "body": "Congratulations on reaching a huge milestone! You might have your first prenatal appointment this week, where you may hear your baby's strong heartbeat—a beautiful reassurance of their progress. It's okay to feel nervous; your medical team is there to support you."
    },
    {
        "week_number": 9,
        "title": "Week 9: Aches and Pains",
        "focus": "Ligaments stretching; minor aches and headaches.",
        "body": "As your uterus starts to grow, you might experience mild cramping or aches. Unless the pain is severe, these are usually just your ligaments stretching to accommodate your growing little one—a sign of healthy expansion."
    },
    {
        "week_number": 10,
        "title": "Week 10: Bloat and Bloating",
        "focus": "Digestive system slowing down, causing bloat.",
        "body": "Don't worry if your belly feels more bloated than pregnant right now; increased progesterone slows down digestion to maximize nutrient absorption for the baby. Embrace loose, comfortable clothes and know this is entirely normal."
    },
    {
        "week_number": 11,
        "title": "Week 11: The Energy Shift Begins",
        "focus": "Approaching the second trimester; symptoms often begin to ease.",
        "body": "You're almost through the first trimester! For many women, this week marks the beginning of symptoms easing up, promising a boost of energy soon. Hold tight, you've done the hardest work of building the foundation."
    },
    {
        "week_number": 12,
        "title": "Week 12: Officially Finishing the First Trimester!",
        "focus": "Biggest milestone reached; risk drops significantly.",
        "body": "You've made it! This is a major celebration—the first trimester is complete, and the risk of miscarriage drops significantly now. Feel proud of your body and look forward to the 'golden weeks' of the second trimester ahead!"
    }
]

# Visit explanation data (Visits 1-4)
VISIT_DATA = [
    {
        "visit_number": 1,
        "typical_week": 8,
        "title": "Visit 1 (Around 8 Weeks): The Confirmation & Plan",
        "purpose": "To officially confirm the pregnancy, review your comprehensive health history, and establish your personalized care plan.",
        "what_happens": "This is often the longest appointment. You'll share detailed health information, get initial blood work done, and your provider may perform an ultrasound to confirm the due date and check your baby's strong heartbeat. It's all about setting up a safe and personalized journey!"
    },
    {
        "visit_number": 2,
        "typical_week": 12,
        "title": "Visit 2 (Around 12 Weeks): First Trimester Checkpoint",
        "purpose": "To discuss optional early screening tests, review initial blood work results, and ensure you are comfortable moving into the second trimester.",
        "what_happens": "Your provider will perform routine checks like measuring your weight and blood pressure. This is a great time to ask any questions you have about managing lingering first-trimester symptoms like nausea or fatigue."
    },
    {
        "visit_number": 3,
        "typical_week": 16,
        "title": "Visit 3 (Around 16 Weeks): Early Second Trimester Check-in",
        "purpose": "To begin monitoring the physical growth of your uterus and confirm that you are settling into the 'golden weeks' of pregnancy.",
        "what_happens": "The provider will likely check your fundal height (measuring your belly) and listen for the baby's heartbeat using a Doppler. Since you often feel much better now, the focus shifts to preparing for your anatomy scan and enjoying the reduced symptoms."
    },
    {
        "visit_number": 4,
        "typical_week": 20,
        "title": "Visit 4 (Around 20 Weeks): Anatomy Scan Review",
        "purpose": "To review the detailed results from your big anatomy scan ultrasound and check in on your baby's movements.",
        "what_happens": "This visit is often filled with excitement as you discuss the detailed pictures of your baby's organs, development, and growth. Your provider will also ask about fetal movement, and you can discuss preparing for the second half of your pregnancy, like birth preparation classes."
    }
]


def seed_weekly_content(db):
    """Seed weekly content for weeks 1-12"""
    print("Seeding weekly content...")
    
    for content_data in WEEKLY_CONTENT_DATA:
        # Check if content already exists
        existing = db.query(WeeklyContent).filter(
            WeeklyContent.week_number == content_data["week_number"]
        ).first()
        
        if not existing:
            content = WeeklyContent(**content_data)
            db.add(content)
            print(f"  ✓ Added Week {content_data['week_number']}: {content_data['title']}")
        else:
            print(f"  - Week {content_data['week_number']} already exists, skipping")
    
    db.commit()
    print("Weekly content seeding complete!\n")


def seed_visit_explanations(db):
    """Seed visit explanation content"""
    print("Seeding visit explanations...")
    
    for visit_data in VISIT_DATA:
        # Check if visit already exists
        existing = db.query(VisitExplanation).filter(
            VisitExplanation.visit_number == visit_data["visit_number"]
        ).first()
        
        if not existing:
            visit = VisitExplanation(**visit_data)
            db.add(visit)
            print(f"  ✓ Added Visit {visit_data['visit_number']}: {visit_data['title']}")
        else:
            print(f"  - Visit {visit_data['visit_number']} already exists, skipping")
    
    db.commit()
    print("Visit explanations seeding complete!\n")


def main():
    """Main seeding function"""
    print("=" * 60)
    print("Maternal Health Monitoring App - Content Seeding Script")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    try:
        seed_weekly_content(db)
        seed_visit_explanations(db)
        
        print("=" * 60)
        print("✓ All content seeded successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error seeding content: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()