#!/usr/bin/env python3
import argparse
import asyncio
import logging
from pathlib import Path
from llm_service import LLMService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class DocUpdater:
    def __init__(self, model_name: str = "llama3.2"):
        logger.info(f"Initializing DocUpdater with model: {model_name}")
        self.llm_service = LLMService(model_name)

    def read_doc_content(self, doc_path: str) -> str:
        """Read content from the documentation file"""
        logger.info(f"Reading documentation from: {doc_path}")
        try:
            path = Path(doc_path)
            if not path.exists():
                logger.error(f"Documentation file not found: {doc_path}")
                raise FileNotFoundError(f"Documentation file not found: {doc_path}")
            content = path.read_text()
            logger.debug(f"Successfully read {len(content)} characters from {doc_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading documentation file: {e}")
            raise RuntimeError(f"Error reading documentation file: {e}")

    def write_doc_content(self, doc_path: str, content: str):
        """Write content back to the documentation file"""
        logger.info(f"Writing updated content to: {doc_path}")
        try:
            path = Path(doc_path)
            path.write_text(content)
            logger.debug(f"Successfully wrote {len(content)} characters to {doc_path}")
        except Exception as e:
            logger.error(f"Error writing to documentation file: {e}")
            raise RuntimeError(f"Error writing to documentation file: {e}")

    async def update_documentation(self, diff_content: str, doc_path: str):
        """Update documentation based on diff content"""
        logger.info("Starting documentation update process")
        logger.debug(f"Received diff content of length: {len(diff_content)}")
        
        try:
            # Read current documentation
            logger.info("Reading current documentation content")
            current_content = self.read_doc_content(doc_path)
            logger.debug(f"Current documentation length: {len(current_content)}")

            # Generate updated content
            logger.info("Generating updated documentation content using LLM")
            updated_content = await self.llm_service.generate_doc_updates(
                current_content,
                diff_content,
                doc_path
            )
            logger.debug(f"Generated updated content length: {len(updated_content)}")

            # Write updated content back to file
            logger.info("Writing updated content back to file")
            self.write_doc_content(doc_path, updated_content)
            logger.info(f"Successfully updated {doc_path}")

        except Exception as e:
            logger.error(f"Error updating documentation: {e}", exc_info=True)
            raise

async def main():
    logger.info("Starting documentation update script")
    
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
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    logger.info(f"Parsed arguments: doc_path={args.doc_path}, model={args.model}")
    logger.debug(f"Diff content length: {len(args.diff)}")

    try:
        logger.info("Creating DocUpdater instance")
        updater = DocUpdater(model_name=args.model)
        
        logger.info("Starting documentation update")
        await updater.update_documentation(args.diff, args.doc_path)
        
        logger.info("Documentation update completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Failed to update documentation: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
