from core.Auditors.Auditor import Auditor
from colorama import Fore
from anthropic import Anthropic

class ClaudeAuditor(Auditor):
    def __init__(self):
        super().__init__()
        pass

    def is_valide(self,key):
        self._debug(f"Claude validating key: {key[:20]}...{key[-10:] if len(key) > 30 else key}")
        
        # Try multiple model names in order of preference
        models = [
            "claude-3-haiku-20240307"
        ]
        
        model_errors = []  # Track errors for each model attempt
        
        for model in models:
            try:
                self._debug(f"Claude initializing client with key prefix: {key[:10]}...")
                client = Anthropic(api_key=key)

                self._debug(f"Claude request: messages.create model={model} key={key[:20]}...")
                message = client.messages.create(
                    model=model,
                    max_tokens=10,
                    messages=[
                        {
                            "role": "user",
                            "content": "Say yes in lowercase only.",
                        },
                    ],
                )
                result = message.content[0].text
                self._debug(f"Claude response: snippet={(str(result)[:200]).replace('\n',' ')}")
                self._debug(f"Claude validation successful for key: {key[:20]}...")
                print(f"{Fore.GREEN}[+] {Fore.WHITE} Valid API found: {key}: {result}")
                return "YES"
            except Exception as e:
                error_str = str(e).lower()
                error_msg = str(e)
                
                # Check if it's a model not found error (404) - this means the API key is valid!
                is_404 = "404" in error_str or ("not_found_error" in error_str and "model:" in error_str)
                model_errors.append(is_404)
                
                if is_404:
                    self._debug(f"Claude model not found (404) for {model}, but API key appears valid. Trying next model...")
                    continue  # Try next model
                
                # Check if it's an authentication error - key is invalid
                if "authentication" in error_str or "401" in error_str or "invalid" in error_str or "api_key" in error_str:
                    self._debug(f"Claude auth error: {e}")
    
                    return "NO"
                
                # Check if it's a rate limit error
                if "rate limit" in error_str or "429" in error_str:
                    self._debug(f"Claude rate limit: {e}")
                    return "NO"
                
                # For other errors, try next model
                self._debug(f"Claude error with model {model}: {error_msg[:100]}, trying next model...")
                continue
        
        # If all models returned 404, the API key is valid (we got proper API responses)
        # but the models don't exist or aren't accessible with this key
        if model_errors and all(model_errors):
            self._debug(f"Claude: All models returned 404, but API key appears valid (got API responses, not auth errors)")
            print(f"{Fore.GREEN}[+] {Fore.WHITE} Valid API found: {key} (Key is valid but models not accessible - may need different model or permissions)")
            return "YES"
        
        # If we've tried all models and got non-404 errors, the key is likely invalid
        self._debug(f"Claude validation failed for all models for key: {key[:20]}...")
        print(f"{Fore.RED}[-] {Fore.WHITE} Invalid API key: {key} (Could not validate with any model)")
        return "NO"

