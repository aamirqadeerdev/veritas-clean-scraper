
import re
import logging
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class DocumentSchema(BaseModel):
    """Defines strict data rules and quality boundaries for AI training sets."""
    source_url: str
    site_id: str
    extracted_text: str = Field(..., min_length=50) # Drop text under 50 characters
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    @field_validator('extracted_text', mode='before')
    @classmethod
    def sanitize_and_scrub_pii(cls, value: str) -> str:
        """Automated GDPR Compliance filter to scrub emails and phone numbers."""
        if not isinstance(value, str):
            return ""

        # Regular Expression pattern for standard email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Regular Expression pattern for standard international phone numbers
        phone_pattern = r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'

        # Replace matching private strings with secure placeholder text
        cleaned_text = re.sub(email_pattern, "[PROTECTED_EMAIL]", value)
        cleaned_text = re.sub(phone_pattern, "[PROTECTED_PHONE]", cleaned_text)
        
        # Remove extra blank lines and spaces to optimize text for LLM token usage
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        return cleaned_text

class DataValidationGateway:
    def process_and_verify(self, raw_data: dict) -> dict:
        """Validates incoming payload against strict structural requirements."""
        try:
            # Pass data into the Pydantic schema for parsing and validation
            validated_doc = DocumentSchema(**raw_data)
            logging.info(f"Validation Gateway: Document successfully certified for AI compilation.")
            return validated_doc.model_dump()
        except Exception as error:
            logging.error(f"Validation Gateway Rejection: Payload dropped due to quality bounds: {error}")
            return {}
