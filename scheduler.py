"""
Scheduler service for running queries at scheduled times.
Uses APScheduler for background task execution.
"""
import logging
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz

logger = logging.getLogger(__name__)

# Turkey timezone (GMT+3)
TIMEZONE = pytz.timezone('Europe/Istanbul')


class QueryScheduler:
    """Manages scheduled query execution."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler = BackgroundScheduler(timezone=TIMEZONE)
        self.db_manager = None
        self.ai_service = None
        logger.info(f"Query scheduler initialized with timezone: {TIMEZONE}")
    
    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            current_time = datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S %Z')
            logger.info(f"🚀 Query scheduler started successfully!")
            logger.info(f"🕐 Current time: {current_time}")
            logger.info(f"🌍 Timezone: {TIMEZONE}")
        else:
            logger.warning("⚠️ Scheduler start() called but already running")
    
    def shutdown(self):
        """Shutdown the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Query scheduler shut down")
    
    def set_services(self, db_manager, ai_service):
        """Set the database manager and AI service."""
        self.db_manager = db_manager
        self.ai_service = ai_service
    
    def add_scheduled_query(self, scheduled_query_id: int, schedule_type: str, 
                           schedule_time: Optional[str] = None, 
                           schedule_day: Optional[int] = None,
                           cron_expression: Optional[str] = None):
        """
        Add a scheduled query to the scheduler.
        
        Args:
            scheduled_query_id: ID of the scheduled query
            schedule_type: Type of schedule (hourly, daily, weekly, monthly, custom)
            schedule_time: Time in HH:MM format
            schedule_day: Day for weekly (0-6) or monthly (1-31)
            cron_expression: Custom cron expression
        """
        job_id = f"scheduled_query_{scheduled_query_id}"
        
        # Remove existing job if any
        self.remove_scheduled_query(scheduled_query_id)
        
        try:
            if schedule_type == "hourly":
                # Run every hour at minute 0
                trigger = CronTrigger(minute=0, timezone=TIMEZONE)
                
            elif schedule_type == "daily":
                # Run daily at specified time
                if not schedule_time:
                    schedule_time = "09:00"
                hour, minute = map(int, schedule_time.split(":"))
                trigger = CronTrigger(hour=hour, minute=minute, timezone=TIMEZONE)
                
            elif schedule_type == "weekly":
                # Run weekly on specified day and time
                if not schedule_time:
                    schedule_time = "09:00"
                if schedule_day is None:
                    schedule_day = 0  # Monday
                hour, minute = map(int, schedule_time.split(":"))
                trigger = CronTrigger(day_of_week=schedule_day, hour=hour, minute=minute, timezone=TIMEZONE)
                
            elif schedule_type == "monthly":
                # Run monthly on specified day and time
                if not schedule_time:
                    schedule_time = "09:00"
                if schedule_day is None:
                    schedule_day = 1  # First day of month
                hour, minute = map(int, schedule_time.split(":"))
                trigger = CronTrigger(day=schedule_day, hour=hour, minute=minute, timezone=TIMEZONE)
                
            elif schedule_type == "custom" and cron_expression:
                # Use custom cron expression
                trigger = CronTrigger.from_crontab(cron_expression, timezone=TIMEZONE)
                
            else:
                logger.error(f"Invalid schedule type: {schedule_type}")
                return False
            
            # Add the job with misfire grace time
            # misfire_grace_time: If a job is late by more than this many seconds, it won't run
            # Setting to None means it will always run even if late
            job = self.scheduler.add_job(
                func=self._execute_scheduled_query,
                trigger=trigger,
                id=job_id,
                args=[scheduled_query_id],
                replace_existing=True,
                misfire_grace_time=3600  # 1 hour grace time
            )
            
            # Log next run time
            if job.next_run_time:
                next_run = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S %Z')
                logger.info(f"✅ Added scheduled query {scheduled_query_id} with type '{schedule_type}' - Next run: {next_run}")
            else:
                logger.warning(f"⚠️ Added scheduled query {scheduled_query_id} but no next_run_time set!")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding scheduled query {scheduled_query_id}: {e}")
            return False
    
    def remove_scheduled_query(self, scheduled_query_id: int):
        """Remove a scheduled query from the scheduler."""
        job_id = f"scheduled_query_{scheduled_query_id}"
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed scheduled query {scheduled_query_id}")
            return True
        except Exception as e:
            # Job might not exist, which is fine
            logger.debug(f"Could not remove job {job_id}: {e}")
            return False
    
    def _execute_scheduled_query(self, scheduled_query_id: int):
        """
        Execute a scheduled query.
        
        Args:
            scheduled_query_id: ID of the scheduled query to execute
        """
        current_time = datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S %Z')
        logger.info(f"🔔 EXECUTING SCHEDULED QUERY #{scheduled_query_id} at {current_time}")
        
        if not self.db_manager or not self.ai_service:
            logger.error("❌ Database manager or AI service not set - Cannot execute query")
            return
        
        try:
            from models import SavedQuery, QueryRequest
            
            # Get the scheduled query details
            scheduled_query = self.db_manager.get_scheduled_query_by_id(scheduled_query_id)
            
            if not scheduled_query or not scheduled_query.is_active:
                logger.warning(f"Scheduled query {scheduled_query_id} not found or inactive")
                return
            
            # Get database schema
            schema = self.db_manager.get_database_schema()
            
            # Create query request
            query_request = QueryRequest(
                question=scheduled_query.question,
                tables=scheduled_query.tables_used
            )
            
            # Convert natural language to SQL
            sql_query = self.ai_service.convert_natural_to_sql(query_request, schema)
            
            # Execute query
            query_response = self.db_manager.execute_query(sql_query)
            
            # Save the query result
            saved_query = SavedQuery(
                question=scheduled_query.question,
                sql_query=sql_query,
                tables_used=scheduled_query.tables_used,
                is_successful=query_response.is_successful,
                error_message=query_response.error,
                query_results=query_response.results if query_response.is_select_query else None,
                result_message=query_response.message,
                is_scheduled=True
            )
            
            query_id = self.db_manager.save_query(saved_query)
            
            # Update scheduled query stats
            status = "success" if query_response.is_successful else "error"
            self.db_manager.update_scheduled_query_run(scheduled_query_id, status)
            
            # Log to backup file
            try:
                import os
                backup_file = "sorgularim.txt"
                file_exists = os.path.exists(backup_file)
                
                with open(backup_file, 'a', encoding='utf-8') as f:
                    if not file_exists:
                        f.write("=" * 80 + "\n")
                        f.write("SQL AGENT - SORGU GEÇMİŞİ\n")
                        f.write("=" * 80 + "\n\n")
                    
                    f.write("\n" + "=" * 80 + "\n")
                    f.write(f"ZAMANLANMIŞ SORGU #{query_id if query_id else 'N/A'} (Schedule ID: {scheduled_query_id})\n")
                    f.write(f"TARİH: {datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
                    f.write(f"DURUM: {'✅ BAŞARILI' if query_response.is_successful else '❌ HATA'}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    f.write(f"📝 SORU:\n{scheduled_query.question}\n\n")
                    f.write(f"📋 TABLOLAR:\n{', '.join(scheduled_query.tables_used)}\n\n")
                    f.write(f"🔍 SQL SORGUSU:\n{sql_query}\n\n")
                    
                    if query_response.is_successful:
                        if query_response.results:
                            f.write(f"📊 SONUÇLAR: {len(query_response.results)} satır\n")
                        elif query_response.message:
                            f.write(f"✅ MESAJ: {query_response.message}\n")
                    else:
                        f.write(f"❌ HATA: {query_response.error}\n")
                    
                    f.write("\n")
                
                logger.info(f"Scheduled query backed up to {backup_file}")
            except Exception as e:
                logger.error(f"Error backing up scheduled query: {e}")
            
            logger.info(f"✅ Scheduled query #{scheduled_query_id} executed successfully! Saved as query ID: {query_id}")
            
        except Exception as e:
            logger.error(f"❌ Error executing scheduled query #{scheduled_query_id}: {e}", exc_info=True)
            # Update with error status
            try:
                self.db_manager.update_scheduled_query_run(scheduled_query_id, "error")
            except Exception as update_err:
                logger.error(f"Failed to update error status: {update_err}")
    
    def load_all_scheduled_queries(self):
        """Load and schedule all active scheduled queries from database."""
        if not self.db_manager:
            logger.error("❌ Database manager not set - Cannot load scheduled queries")
            return
        
        try:
            scheduled_queries = self.db_manager.get_all_scheduled_queries(active_only=True)
            
            if not scheduled_queries:
                logger.info("ℹ️ No active scheduled queries found in database")
                return
            
            logger.info(f"📋 Loading {len(scheduled_queries)} active scheduled queries...")
            
            success_count = 0
            for sq in scheduled_queries:
                logger.info(f"  - Loading query #{sq.id}: {sq.question[:50]}... ({sq.schedule_type})")
                result = self.add_scheduled_query(
                    scheduled_query_id=sq.id,
                    schedule_type=sq.schedule_type,
                    schedule_time=sq.schedule_time,
                    schedule_day=sq.schedule_day,
                    cron_expression=sq.cron_expression
                )
                if result:
                    success_count += 1
            
            logger.info(f"✅ Successfully loaded {success_count}/{len(scheduled_queries)} scheduled queries")
            
        except Exception as e:
            logger.error(f"❌ Error loading scheduled queries: {e}", exc_info=True)


# Global scheduler instance
query_scheduler = QueryScheduler()

