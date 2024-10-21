import requests

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
