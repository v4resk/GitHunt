from core.Dorks.Dorks import Dorks
import re

class PerplexityDorks(Dorks):
    def __init__(self):
        super().__init__()
        self.keywords = [
            "CoT",
            "DPO",
            "RLHF",
            "agent",
            "ai model",
            "aios",
            "api key",
            "apikey",
            "artificial intelligence",
            "chain of thought",
            "chatbot",
            "chatgpt",
            "competitor analysis",
            "content strategy",
            "conversational AI",
            "data analysis",
            "deep learning",
            "direct preference optimization",
            "experiment",
            "gpt",
            "gpt-3",
            "gpt-4",
            "gpt4",
            "key",
            "keyword clustering",
            "keyword research",
            "lab",
            "language model experimentation",
            "large language model",
            "llama.cpp",
            "llm",
            "long-tail keywords",
            "machine learning",
            "multi-agent",
            "multi-agent systems",
            "natural language processing",
            "openai",
            "personalized AI",
            "project",
            "rag",
            "reinforcement learning from human feedback",
            "retrieval-augmented generation",
            "search intent",
            "semantic search",
            "thoughts",
            "virtual assistant",
            "实验",
            "密钥",
            "测试",
            "语言模型",
        ]

        self.languages = [
            '"Jupyter Notebook"',
            "Python",
            "Shell",
            "JavaScript",
            "TypeScript",
            "Java",
            "Go",
            "C%2B%2B",
            "PHP",
        ]

        self.regex_list = [
            re.compile(r"pplx-[a-zA-Z0-9]{40,}"),  # Perplexity API Key
        ]