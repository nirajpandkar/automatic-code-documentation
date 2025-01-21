#!/usr/bin/env python3
import argparse
import asyncio
from pathlib import Path
from llm_service import LLMService

class DocUpdater:
    def __init__(self, model_name: str = "llama3.2"):
        self.llm_service = LLMService(model_name)

    def read_doc_content(self, doc_path: str) -> str:
        """Read content from the documentation file"""
        try:
            path = Path(doc_path)
            if not path.exists():
                raise FileNotFoundError(f"Documentation file not found: {doc_path}")
            return path.read_text()
        except Exception as e:
            raise RuntimeError(f"Error reading documentation file: {e}")

    def write_doc_content(self, doc_path: str, content: str):
        """Write content back to the documentation file"""
        try:
            path = Path(doc_path)
            path.write_text(content)
        except Exception as e:
            raise RuntimeError(f"Error writing to documentation file: {e}")

    async def update_documentation(self, diff_content: str, doc_path: str):
        """Update documentation based on diff content"""
        try:
            # Read current documentation
            current_content = self.read_doc_content(doc_path)

            # Generate updated content
            updated_content = await self.llm_service.generate_doc_updates(
                current_content,
                diff_content,
                doc_path
            )

            # Write updated content back to file
            self.write_doc_content(doc_path, updated_content)
            print(f"Successfully updated {doc_path}")

        except Exception as e:
            print(f"Error updating documentation: {e}")
            raise

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Update documentation based on staged changes')
    parser.add_argument(
        '--diff', 
        required=True,
        help='Git diff content of staged changes'
    )
    parser.add_argument(
        '--doc-path', 
        default='README.md',
        help='Path to documentation file (default: README.md)'
    )
    parser.add_argument(
        '--model',
        default='llama3.2',
        help='Name of the Ollama model to use (default: llama3.2)'
    )

    args = parser.parse_args()

    try:
        updater = DocUpdater(model_name=args.model)
        await updater.update_documentation(args.diff, args.doc_path)
    except Exception as e:
        print(f"Failed to update documentation: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
