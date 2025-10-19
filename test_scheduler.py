"""
Test script to check scheduler status and trigger immediate execution.
Run this to debug and test scheduled queries.

Usage:
    python test_scheduler.py                      # Check scheduler status
    python test_scheduler.py <query_id>           # Trigger specific query
    python test_scheduler.py --setup              # Setup test database connection
"""
import logging
import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Add the current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scheduler import query_scheduler, TIMEZONE
from datetime import datetime

# Setup logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_scheduler_status():
    """Check if scheduler is running and list all jobs."""
    print("\n" + "="*80)
    print("🔍 SCHEDULER STATUS CHECK")
    print("="*80)
    
    # Check if running
    is_running = query_scheduler.scheduler.running
    print(f"\n📊 Scheduler Running: {'✅ YES' if is_running else '❌ NO'}")
    
    # Current time
    current_time = datetime.now(TIMEZONE)
    print(f"🕐 Current Time (Turkey): {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # List all jobs
    jobs = query_scheduler.scheduler.get_jobs()
    print(f"\n📋 Total Jobs Scheduled: {len(jobs)}")
    
    if jobs:
        print("\n" + "-"*80)
        for job in jobs:
            print(f"\n🔹 Job ID: {job.id}")
            print(f"   Function: {job.func_ref}")
            print(f"   Next Run: {job.next_run_time}")
            print(f"   Trigger: {job.trigger}")
            
            # Calculate time until next run
            if job.next_run_time:
                time_diff = job.next_run_time - current_time
                total_seconds = int(time_diff.total_seconds())
                
                if total_seconds > 0:
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    print(f"   ⏰ Time Until Run: {hours}h {minutes}m {seconds}s")
                else:
                    print(f"   ⚠️  Next run is {abs(total_seconds)} seconds in the past!")
        print("-"*80)
    else:
        print("\n⚠️  No jobs found! Make sure you:")
        print("   1. Have created a scheduled query")
        print("   2. The query is ACTIVE")
        print("   3. Database connection is established")
    
    print("\n" + "="*80 + "\n")

def trigger_job_now(scheduled_query_id: int):
    """Manually trigger a scheduled query immediately."""
    print(f"\n🚀 Triggering scheduled query #{scheduled_query_id} NOW...")
    
    try:
        query_scheduler._execute_scheduled_query(scheduled_query_id)
        print(f"✅ Query #{scheduled_query_id} executed successfully!")
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        logger.error(f"Error: {e}", exc_info=True)

def setup_scheduler_with_db():
    """Setup scheduler with database connection for testing."""
    print("\n" + "="*80)
    print("🔧 SETTING UP SCHEDULER WITH DATABASE CONNECTION")
    print("="*80 + "\n")
    
    try:
        from database import DatabaseManager
        from ai_service import AIService
        from config import Config
        
        # Validate config
        Config.validate_config()
        
        # Prompt for database connection
        print("Please provide database connection string:")
        print("Example: DRIVER={SQL Server};SERVER=localhost;DATABASE=mydb;UID=user;PWD=pass")
        connection_string = input("\nConnection String: ").strip()
        
        if not connection_string:
            print("❌ Connection string cannot be empty")
            return False
        
        # Create database manager
        db_manager = DatabaseManager(connection_string)
        
        # Test connection
        print("\n🔍 Testing database connection...")
        if not db_manager.test_connection():
            print("❌ Database connection failed")
            return False
        
        print("✅ Database connection successful")
        
        # Setup scheduler services
        ai_service = AIService()
        query_scheduler.set_services(db_manager, ai_service)
        print("✅ Scheduler services configured")
        
        # Start scheduler
        if not query_scheduler.scheduler.running:
            query_scheduler.start()
            print("✅ Scheduler started")
        
        # Load scheduled queries
        print("\n📋 Loading scheduled queries from database...")
        query_scheduler.load_all_scheduled_queries()
        
        print("\n✅ Setup complete! Scheduler is ready.")
        return True
        
    except Exception as e:
        logger.error(f"Setup failed: {e}", exc_info=True)
        print(f"\n❌ Setup failed: {e}")
        return False


if __name__ == "__main__":
    
    # Check for --setup flag
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        success = setup_scheduler_with_db()
        if success:
            check_scheduler_status()
        sys.exit(0 if success else 1)
    
    # Check status
    check_scheduler_status()
    
    # If query ID provided, trigger it
    if len(sys.argv) > 1:
        try:
            query_id = int(sys.argv[1])
            
            # Check if scheduler has services configured
            if not query_scheduler.db_manager or not query_scheduler.ai_service:
                print("\n⚠️  WARNING: Scheduler services not configured!")
                print("Run with --setup flag first: python test_scheduler.py --setup")
                print("\nAttempting to trigger anyway (may fail)...")
            
            trigger_job_now(query_id)
        except ValueError:
            print("❌ Invalid query ID. Usage: python test_scheduler.py [query_id]")
            print("\nAvailable commands:")
            print("  python test_scheduler.py                 # Check status")
            print("  python test_scheduler.py <query_id>      # Trigger query")
            print("  python test_scheduler.py --setup         # Setup with DB")
    else:
        print("\n💡 TIPS:")
        print("  • To manually trigger a query:")
        print("    python test_scheduler.py <scheduled_query_id>")
        print("\n  • To setup scheduler with database:")
        print("    python test_scheduler.py --setup")

