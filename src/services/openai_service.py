from openai import OpenAI
import dotenv
import os
dotenv.load_dotenv()

def get_llm_prompt(query: str) -> str:
    return f"Take the given query `{query}` and augment it to be more detailed. For example, add specific names, types, embellishments, richness. Do not make it longer than 12 words."


class OpenAIAugment():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        print(f"OpenAI API Key: {self.client.api_key}")

    def augment_query(self, query: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "user",
                    "content": get_llm_prompt(query)
                }
            ],
            temperature=0.9,
            max_tokens=64,
            top_p=1,
        )
        return response.choices[0].message.content.strip("\"").strip("'")
