> This document itself started off blank and has been updated by the tool. For example you can see commit [00d44bb](https://github.com/nirajpandkar/automatic-code-documentation/commit/00d44bb4632e96f93d84f141bdcffff5a2f42f68) for how it added incremental documentation for the logging functionality added in the code.

# Core Components

The core components of this tool are - 

1. Post-add alias
2. LLM Integration Service
    a. Documentation Update Handler (Updating docs)

## Post-add alias

```bash
git config --global alias.update-and-add '!git add "$@"; ./post_add.sh "$(git diff --cached)";'
```

## LLM Integration Service

### Documentation Update Handler (Updating docs)
The `DocUpdater` class is responsible for updating the documentation based on the provided diff content. It uses the `LLMService` to generate updated content and writes it back to the original documentation file.
Argument parsing has been added for the diff content, doc path, model name, and debug flag.

### Logging Configuration
The script now uses a logging configuration with a basic format and level. It also sets up a logger instance and enables debug logging if requested via the `--debug` argument.

## Documentation Update Process
The documentation update process involves reading the current documentation content, generating updated content using the LLMService, writing the updated content back to the file, and handling any exceptions that may occur during the process.

# Features TBD

## Identify the documents to be updated instead of hardcoding
This will essentially identify the documents that need updating by looking at the staged diff. Will maybe require RAG?

## Giving context to the staged diff
Currently only the staged diff is given in a prompt to the LLM. What if the relevant code around it was also provided as a context. Would it allow the LLM to understand the nuance of change and hence generate better documentation updates?
