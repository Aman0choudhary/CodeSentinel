from typing import Optional
import requests


class HermesClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        api_path: str,
        timeout_seconds: int,
        enabled: bool,
        verbose: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.api_path = api_path
        self.timeout_seconds = timeout_seconds
        self.enabled = enabled and bool(self.base_url)
        self.verbose = verbose

    def run(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        url = f"{self.base_url}{self.api_path}"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout_seconds)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict):
            choices = data.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                return message.get("content", "")
            if "content" in data:
                return data.get("content", "")

        return ""
