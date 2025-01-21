# llm_service.py
import ollama
from typing import List, Dict, Optional

class LLMService:
    def __init__(self, model_name: str = "llama3.2"):
        self.model = model_name
    
    async def _call_llm(self, prompt: str) -> str:
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")

    async def identify_affected_docs(self, diff_content: str, docs_directory: str) -> List[str]:
        prompt = f"""
        Analyze this git diff and identify which markdown files in the {docs_directory} 
        directory need to be updated. Return only the file paths, one per line.
        
        Git diff:
        {diff_content}
        """
        
        response = await self._call_llm(prompt)
        return [path.strip() for path in response.split('\n') if path.strip()]
    
    async def generate_doc_updates(
        self, 
        current_docs: str, 
        diff_content: str,
        file_path: str
    ) -> str:
        prompt = f"""
        Update the following documentation based on the code changes.
        Keep the same markdown structure and formatting.
        Only modify sections that need updating based on the code changes.
        Be very brief regarding the changes.
        Don't include code in the generated documentation.

        Documentation file content:
        {current_docs}
        
        Code changes:
        {diff_content}
        """
        
        return await self._call_llm(prompt)