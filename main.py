from extraction import EmailFetcher
from support import AIPersonalAssistant
from dotenv import load_dotenv
import asyncio
import logging
import signal
import sys
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('email_assistant.log')
    ]
)
logger = logging.getLogger(__name__)

class EmailAssistantService:
    def __init__(self):
        self.is_running = True
        self.fetcher: Optional[EmailFetcher] = None
        self.ai_assistant: Optional[AIPersonalAssistant] = None

    def setup(self):
        """Initialize the email fetcher and AI assistant"""
        load_dotenv()
        self.fetcher = EmailFetcher()
        # Replace with your preferred HuggingFace model
        self.ai_assistant = AIPersonalAssistant(huggingface_model="google/flan-t5-base")
        
        # Setup signal handlers for graceful shutdown
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, self._shutdown_handler)

    def _shutdown_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("Shutdown signal received. Cleaning up...")
        self.is_running = False

    async def process_single_email(self, email_message, sender_name, sender_addr):
        """Process a single email with error handling"""
        try:
            if sender_addr not in self.fetcher.whitelist:
                logger.info(f"Ignored email from: {sender_name} ({sender_addr}) - Not in whitelist")
                return

            logger.info(f"Processing email from: {sender_name} ({sender_addr})")
            extracted_properties, evaluation_result = await self.ai_assistant.process_email(
                email_message
            )

            subject = "AI Personal Assistant Reply"
            self.fetcher.send_email(sender_addr, subject, evaluation_result)
            logger.info(f"Successfully processed and replied to email from {sender_addr}")

        except Exception as e:
            logger.error(f"Error processing email from {sender_addr}: {str(e)}")
            # Optionally send error notification to admin
            # self.fetcher.send_error_notification(f"Error processing email: {str(e)}")

    async def run(self):
        """Main service loop"""
        logger.info("Starting Email Assistant Service")
        
        while self.is_running:
            try:
                logger.info("Checking for new emails...")
                new_emails = await self.fetcher.fetch_new_emails()
                
                # Process emails concurrently
                tasks = [
                    self.process_single_email(email_message, sender_name, sender_addr)
                    for email_message, sender_name, sender_addr in new_emails
                ]
                
                if tasks:
                    await asyncio.gather(*tasks)
                
                logger.info("Waiting for next check cycle...")
                await asyncio.sleep(10)

            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                # Wait a bit before retrying in case of persistent errors
                await asyncio.sleep(30)

        logger.info("Service shutdown complete")

async def main():
    """Entry point of the application"""
    try:
        service = EmailAssistantService()
        service.setup()
        await service.run()
    except Exception as e:
        logger.critical(f"Critical error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())