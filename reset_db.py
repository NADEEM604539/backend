#!/usr/bin/env python3
"""
Reset database script - drops and recreates the library database
"""
from sqlalchemy import create_engine, text
import sys

def reset_database():
    """Drop and recreate the database"""
    try:
        # Connect to MySQL without specifying database
        engine = create_engine(
            f"mysql+pymysql://root:NdM604539@127.0.0.1:3306/mysql",
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        
        with engine.connect() as conn:
            # Drop existing database
            conn.execute(text("DROP DATABASE IF EXISTS library"))
            conn.commit()
            print("✓ Database dropped successfully")
            
            # Create new database
            conn.execute(text("CREATE DATABASE library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
            print("✓ Database created successfully")
        
        engine.dispose()  # Close all connections
        
        # Now create new engine for app database
        app_engine = create_engine(
            "mysql+pymysql://root:NdM604539@127.0.0.1:3306/library",
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        
        # Import all models to register them
        from models import (
            User, RolePermission, LibraryPolicy, Author, Category,
            Book, IssueRecord, UserFine, Notification, SystemLog, PerformanceBenchmark, Base
        )
        
        # Create all tables
        Base.metadata.create_all(bind=app_engine)
        print("✓ All tables created successfully")
        
        # Insert default library policy
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=app_engine)
        session = Session()
        
        policy = LibraryPolicy(
            policy_id=1,
            max_books_per_user=5,
            max_issue_days=14,
            fine_per_day=10.0,
            grace_period_days=0,
            lost_book_penalty_multiplier=2.5,
            max_renewals=2
        )
        session.add(policy)
        session.commit()
        print("✓ Default library policy inserted")
        
        session.close()
        app_engine.dispose()
        print("\n✅ Database reset complete! Ready for data insertion.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = reset_database()
    sys.exit(0 if success else 1)
