import requests
import dotenv

class Ollama:
    def __init__(self, model:str, endpoint: str = "http://localhost:11434/api/generate") -> None:
        self.endpoint = endpoint
        self.model = model

    def invoke(self, prompt: str) -> str:
        try:
            r = requests.post(
                self.endpoint,
                json={"model": self.model, "prompt": prompt, "stream": False}
            )

        except Exception as e:
            print(e)
            return ""

        return r.json()["response"]

class Groq:
    def __init__(self, model:str) -> None:
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        self.model = model
        self.api_key = dotenv.dotenv_values(".env")["GROQ_API_KEY"]

    def invoke(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            r = requests.post(
                url=self.endpoint,
                headers=headers,
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                },
            )

        except Exception as e:
            print(e)
            return ""

        return r.json()["choices"][0]["message"]["content"]
