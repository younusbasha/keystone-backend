"""
Google Gemini AI Service
"""
import asyncio
import json
from typing import Dict, List, Optional, Any
from google import genai
from google.genai import types
import structlog

from app.config.settings import get_settings
from app.core.exceptions import BaseAPIException

settings = get_settings()
logger = structlog.get_logger(__name__)

class AIServiceException(BaseAPIException):
    """Raised when AI service operations fail"""
    pass

class GeminiService:
    """Service for interacting with Google Gemini AI"""

    def __init__(self):
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Gemini client"""
        try:
            if not settings.GOOGLE_AI_API_KEY:
                logger.warning("Google AI API key not configured")
                return

            self.client = genai.Client(api_key=settings.GOOGLE_AI_API_KEY)
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize Gemini client", error=str(e))
            raise AIServiceException(f"Failed to initialize Gemini client: {str(e)}")

    async def analyze_requirement(self, requirement_text: str) -> Dict[str, Any]:
        """Analyze requirement text and extract information"""
        if not self.client:
            raise AIServiceException("Gemini client not initialized")

        prompt = f"""
        Analyze the following software requirement and provide a structured analysis:

        Requirement: {requirement_text}

        Please provide a JSON response with the following structure:
        {{
            "entities": [
                {{
                    "type": "feature|component|integration|data_model",
                    "name": "entity name",
                    "description": "brief description"
                }}
            ],
            "features": ["list of main features identified"],
            "complexity_assessment": "low|medium|high",
            "effort_estimate": "estimated hours (integer)",
            "confidence_score": "confidence in analysis (0.0-1.0)",
            "suggestions": ["list of implementation suggestions"],
            "risks": ["list of potential risks or challenges"],
            "acceptance_criteria": ["suggested acceptance criteria"],
            "tech_considerations": ["technical considerations"]
        }}

        Focus on practical software development aspects and be specific.
        """

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=settings.DEFAULT_AI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.AI_TEMPERATURE,
                    max_output_tokens=settings.AI_MAX_TOKENS
                )
            )

            # Parse the response
            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:-3]  # Remove markdown code blocks

            analysis = json.loads(result_text)

            logger.info("Requirement analysis completed", confidence=analysis.get("confidence_score"))
            return analysis

        except json.JSONDecodeError as e:
            logger.error("Failed to parse Gemini response as JSON", error=str(e))
            # Return a basic analysis if parsing fails
            return {
                "entities": [],
                "features": [],
                "complexity_assessment": "medium",
                "effort_estimate": 8,
                "confidence_score": 0.5,
                "suggestions": ["Manual analysis required - AI parsing failed"],
                "risks": ["Unable to perform detailed analysis"],
                "acceptance_criteria": [],
                "tech_considerations": []
            }
        except Exception as e:
            logger.error("Requirement analysis failed", error=str(e))
            raise AIServiceException(f"Requirement analysis failed: {str(e)}")

    async def generate_tasks(self, requirement: Dict[str, Any], max_tasks: int = 10) -> List[Dict[str, Any]]:
        """Generate tasks from requirement analysis"""
        if not self.client:
            raise AIServiceException("Gemini client not initialized")

        prompt = f"""
        Based on the following requirement analysis, generate a list of development tasks:

        Requirement Title: {requirement.get('title', 'N/A')}
        Description: {requirement.get('description', 'N/A')}
        Analysis: {json.dumps(requirement.get('ai_analysis', {}), indent=2)}

        Generate maximum {max_tasks} tasks in JSON format:
        {{
            "tasks": [
                {{
                    "title": "Task title",
                    "description": "Detailed task description",
                    "type": "feature|bug|enhancement|documentation|testing|devops",
                    "priority": "low|medium|high|critical",
                    "estimated_hours": "integer estimate",
                    "dependencies": ["list of task titles this depends on"],
                    "acceptance_criteria": ["specific criteria for completion"]
                }}
            ]
        }}

        Include tasks for:
        - Core implementation
        - Unit testing
        - Integration testing
        - Documentation
        - Code review

        Make tasks specific and actionable.
        """

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=settings.DEFAULT_AI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.AI_TEMPERATURE,
                    max_output_tokens=settings.AI_MAX_TOKENS
                )
            )

            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:-3]

            result = json.loads(result_text)
            tasks = result.get("tasks", [])

            logger.info("Task generation completed", task_count=len(tasks))
            return tasks

        except Exception as e:
            logger.error("Task generation failed", error=str(e))
            raise AIServiceException(f"Task generation failed: {str(e)}")

# Global service instance
gemini_service = GeminiService()
