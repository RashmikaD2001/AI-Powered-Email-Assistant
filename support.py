from langchain.schema import Document
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatHuggingFace
from langchain.prompts import PromptTemplate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import json
import os
from langchain_community.llms import HuggingFacePipeline

class AIPersonalAssistant:
    def __init__(self, huggingface_model: str):
        self.hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_API_TOKEN environment variable is required")

        self.huggingface_model = huggingface_model
        model = AutoModelForSeq2SeqLM.from_pretrained(huggingface_model)
        tokenizer = AutoTokenizer.from_pretrained(huggingface_model)
        
        # Create text generation pipeline
        self.pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1  # Use CPU
        )
        
        # Initialize the chat model correctly
        self.chat_model = HuggingFacePipeline(pipeline=self.pipeline)
        
        self.properties = [
            {
                "name": "category",
                "description": "The type of email this is.",
                "type": "string",
                "enum": ["personal", "educational", "reminder", "general_inquiry", "task_update", "other"],
                "required": True,
            },
            {
                "name": "mentioned_topic",
                "description": "The topic mentioned in this email.",
                "type": "string",
                "required": True,
            },
            {
                "name": "message_summary",
                "description": "A brief summary of the email content.",
                "type": "string",
                "required": True,
            },
            {
                "name": "name",
                "description": "Name of the person who wrote the email",
                "type": "string",
                "required": True,
            },
        ]

    def extract_properties(self, content: str) -> dict:
        extraction_prompt = f"""
        Analyze the following email content and extract these properties:
        {json.dumps(self.properties, indent=2)}

        Email content:
        {content}

        Provide the extracted properties in JSON format.
        """

        try:
            # Use the pipeline directly for property extraction
            raw_output = self.pipeline(extraction_prompt, max_length=512, do_sample=True)[0]['generated_text']
            print(f"Raw output: {raw_output}")  # Log the raw output for debugging

            # Try to extract valid JSON from the raw output
            json_start = raw_output.find('{')  # Find the first `{` to ensure valid JSON
            json_end = raw_output.rfind('}') + 1  # Find last `}` to close JSON

            if json_start != -1 and json_end != -1:
                extracted_properties = json.loads(raw_output[json_start:json_end])
            else:
                raise ValueError("No valid JSON found in the output")

        except Exception as e:
            print(f"Error in property extraction: {str(e)}")
            extracted_properties = {
                "category": "other",
                "mentioned_topic": "unknown",
                "message_summary": content[:100] + "...",
                "name": "user"
            }

        return extracted_properties

    def interpret_and_evaluate(self, extracted_properties: dict) -> str:
        response_prompt = f"""
        Generate a friendly email response.
        User name: {extracted_properties['name']}
        Category: {extracted_properties['category']}
        Topic: {extracted_properties['mentioned_topic']}
        Summary: {extracted_properties['message_summary']}

        Write a response that acknowledges the message, offers help, and includes a polite closing.
        Sign the email as Rashmika Dushmantha.
        """

        try:
            # Use the pipeline directly for response generation
            result = self.pipeline(response_prompt, max_length=512, do_sample=True)[0]['generated_text']
        except Exception as e:
            print(f"Error in response generation: {str(e)}")
            result = f"""
            Dear {extracted_properties['name']},

            Thank you for your email. I apologize, but I am currently experiencing some technical difficulties. 
            I will get back to you as soon as possible.

            Best regards,
            Rashmika D7621
            """
        
        return result

    def get_email_content(self, email_message) -> str:
        maintype = email_message.get_content_maintype()
        if maintype == "multipart":
            for part in email_message.get_payload():
                if part.get_content_maintype() == "text":
                    return part.get_payload()
        elif maintype == "text":
            return email_message.get_payload()
        return ""

    async def process_email(self, email_message):
        email_content = self.get_email_content(email_message)
        extracted_properties = self.extract_properties(email_content)
        evaluation_result = self.interpret_and_evaluate(extracted_properties)
        return extracted_properties, evaluation_result



'''
from langchain.schema import Document
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatHuggingFace
from langchain.prompts import PromptTemplate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import json
import os
from langchain_community.llms import HuggingFacePipeline


class AIPersonalAssistant:
    def __init__(self, huggingface_model: str):
        self.hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_API_TOKEN environment variable is required")

        self.huggingface_model = huggingface_model
        model = AutoModelForSeq2SeqLM.from_pretrained(huggingface_model)
        tokenizer = AutoTokenizer.from_pretrained(huggingface_model)
        
        # Create text generation pipeline
        self.pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1  # Use CPU
        )
        
        # Initialize the chat model correctly
        self.chat_model = HuggingFacePipeline(pipeline=self.pipeline)
        
        self.properties = [
            {
                "name": "category",
                "description": "The type of email this is.",
                "type": "string",
                "enum": ["personal", "educational", "reminder", "general_inquiry", "task_update", "other"],
                "required": True,
            },
            {
                "name": "mentioned_topic",
                "description": "The topic mentioned in this email.",
                "type": "string",
                "required": True,
            },
            {
                "name": "message_summary",
                "description": "A brief summary of the email content.",
                "type": "string",
                "required": True,
            },
            {
                "name": "name",
                "description": "Name of the person who wrote the email",
                "type": "string",
                "required": True,
            },
        ]

    def extract_properties(self, content: str) -> dict:
        extraction_prompt = f"""
        Analyze the following email content and extract these properties:
        {json.dumps(self.properties, indent=2)}

        Email content:
        {content}

        Provide the extracted properties in JSON format.
        """

        # try:
        #     # Use pipeline directly for property extraction
        #     result = self.pipeline(extraction_prompt, max_length=512, do_sample=True)[0]['generated_text']
        #     extracted_properties = json.loads(result)
        # except Exception as e:
        #     print(f"Error in property extraction: {str(e)}")
        #     extracted_properties = {
        #         "category": "other",
        #         "mentioned_topic": "unknown",
        #         "message_summary": content[:100] + "...",
        #         "name": "user"
        #     }

        try:
            raw_output = self.pipeline(extraction_prompt, max_length=512, do_sample=True)[0]['generated_text']
            json_start = raw_output.find('{')  # Find the first `{` to ensure valid JSON
            json_end = raw_output.rfind('}') + 1  # Find last `}` to close JSON
            extracted_properties = json.loads(raw_output[json_start:json_end])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}, Raw output: {raw_output}")
            extracted_properties = {
                "category": "other",
                "mentioned_topic": "unknown",
                "message_summary": content[:100] + "...",
                "name": "user"
            }

        return extracted_properties

    def interpret_and_evaluate(self, extracted_properties: dict) -> str:
        response_prompt = f"""
        Generate a friendly email response.
        User name: {extracted_properties['name']}
        Category: {extracted_properties['category']}
        Topic: {extracted_properties['mentioned_topic']}
        Summary: {extracted_properties['message_summary']}

        Write a response that acknowledges the message, offers help, and includes a polite closing.
        Sign the email as Alex.
        """

        try:
            # Use pipeline directly for response generation
            result = self.pipeline(response_prompt, max_length=1000, do_sample=True)[0]['generated_text']
        except Exception as e:
            print(f"Error in response generation: {str(e)}")
            result = f"""
            Dear {extracted_properties['name']},

            Thank you for your email. I apologize, but I am currently experiencing some technical difficulties. 
            I will get back to you as soon as possible.

            Best regards,
            Alex
            """
        
        return result

    def get_email_content(self, email_message) -> str:
        maintype = email_message.get_content_maintype()
        if maintype == "multipart":
            for part in email_message.get_payload():
                if part.get_content_maintype() == "text":
                    return part.get_payload()
        elif maintype == "text":
            return email_message.get_payload()
        return ""

    async def process_email(self, email_message):
        email_content = self.get_email_content(email_message)
        extracted_properties = self.extract_properties(email_content)
        evaluation_result = self.interpret_and_evaluate(extracted_properties)
        return extracted_properties, evaluation_result
'''