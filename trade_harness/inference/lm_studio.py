import logging
import json
from openai import AsyncOpenAI
from trade_harness.config import LM_STUDIO_URL

logger = logging.getLogger("trade_harness.inference")

class LMStudioClient:
    def __init__(self, base_url: str = LM_STUDIO_URL):
        self.base_url = base_url
        self.client = AsyncOpenAI(base_url=self.base_url, api_key="lm-studio")

    async def generate_decision(self, prompt: str) -> dict:
        try:
            logger.info("Sending prompt to local LM Studio...")
            response = await self.client.chat.completions.create(
                model="gemma-4-e2b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                timeout=10.0
            )
            raw_content = response.choices[0].message.content.strip()
            # Clean possible markdown formatting in response
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
            raw_content = raw_content.strip()
            
            return json.loads(raw_content)
        except Exception as e:
            logger.warning(f"LM Studio call failed or was offline: {e}. Falling back to default HOLD signal.")
            # Fallback mock response for testing/development
            return {
                "action": "HOLD",
                "confidence": 0.0,
                "reasoning": f"LM Studio offline or error: {str(e)}",
                "sl_price": 0.0,
                "tp_price": 0.0
            }
