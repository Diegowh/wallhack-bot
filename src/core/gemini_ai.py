import google.generativeai as genai
import google.generativeai.types
from config.config import GOOGLE_API_KEY
import asyncio


class GeminiAI:

    def __init__(self, api_key: str = GOOGLE_API_KEY):
        self.api_key: str = api_key
        self.configure_api_key()
        self.generative_models = self.get_generative_models()
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="You are a discord bot. "
                               "Be concise and witty, but don't be too offensive. "
                               "One sentence response is enough. "
                               "Respond in the same language as the prompt. "
        )

    @staticmethod
    def get_generative_models():
        return [model for model in genai.list_models() if 'generateContent' in model.supported_generation_methods]

    def configure_api_key(self):
        genai.configure(api_key=self.api_key)

    async def generate_response(self, prompt: str, max_tokens: int = 25):
        generation_config = google.generativeai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            response_mime_type="text/plain"
        )
        response: google.generativeai.types.AsyncGenerateContentResponse = \
            await self.model.generate_content_async(contents=prompt, generation_config=generation_config)
        return response.text


if __name__ == "__main__":

    test_api_key = ""
    ai = GeminiAI(api_key=test_api_key)
    question = "How are you today?"
    r = asyncio.run(ai.generate_response(prompt=question))
    print(r)
