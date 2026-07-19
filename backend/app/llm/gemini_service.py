from google import genai

from app.core.config import settings
from app.core.logger import logger


class GeminiService:
    """
    Handles all interactions with the Gemini model.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model = settings.GEMINI_MODEL

    def generate_answer(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate a final answer using the provided context.
        """

        logger.info("Generating response with Gemini.")

        prompt = self._build_prompt(
            query=query,
            context=context,
        )
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
        except Exception as e:
            logger.exception(...)
            raise

        answer = response.text.strip()

        logger.info("Answer generated successfully.")

        return answer

    def judge_context(
        self,
        query: str,
        context: str,
    ) -> bool:
        """
        Determine whether the retrieved context contains
        enough information to answer the user's question.
        """

        logger.info("Evaluating retrieved context with Gemini.")

        prompt = f"""
You are evaluating a Retrieval-Augmented Generation (RAG) system.

Your task is NOT to answer the user's question.

Determine whether the provided context contains enough
information to answer the user's question accurately.

Question:
{query}

Retrieved Context:
{context}

Respond with ONLY one word.

YES
or
NO
"""
        try: 
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
        except Exception as e:
            logger.exception(...)
            raise

        answer = response.text.strip().upper()

        logger.info(f"Gemini Context Judge: {answer}")

        return answer.startswith("YES")

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Build the prompt used for answer generation.
        """

        return f"""
You are an AI-powered Study Assistant.

Your goal is to answer the user's question using ONLY the provided context.

The context may come from:
- Uploaded study materials
- Trusted web search results
- Or both

Instructions:

1. Answer only from the provided context.
2. Do NOT use your own knowledge.
3. If the answer is not available in the context, clearly state that the information is unavailable in the retrieved context.
4. Be accurate and concise.
5. When appropriate, explain concepts step by step.
6. Use bullet points when they improve readability.

Retrieved Context:
{context}

User Question:
{query}

Answer:
"""