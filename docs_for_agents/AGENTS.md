# Project instructions

## Communication

* Communicate with me in Czech.
* Explain decisions, proposed changes, and results in Czech.
* Keep code, variable names, function names, class names, and other identifiers in English.
* Write code comments in Czech unless an English comment is conventional or required by a library.

## Working style

* I am a data scientist/statistician, not a professional software developer.
* Prefer clear, readable, maintainable Python over unnecessarily sophisticated solutions.
* Do not introduce abstractions, classes, functions, or dependencies unless they provide a clear benefit.
* Preserve the existing project structure unless there is a good reason to change it.
* When several technically valid approaches exist, briefly explain the alternatives and recommend one.

## Before making changes

* For non-trivial changes, first inspect the relevant files and understand the existing implementation.
* Before making substantial modifications, explain briefly what you intend to change and why.
* Do not modify unrelated files.
* Do not change the behavior of existing code unless this is explicitly requested or necessary to fix a documented problem.
* If a requested change could affect existing behavior, point this out before implementing it.

## Safety

* Do not delete files or overwrite important files without asking for confirmation.
* Do not change configuration, dependencies, or project structure unnecessarily.
* Never expose, print, commit, or modify API keys, passwords, tokens, or other secrets.
* Before a large refactoring, recommend creating a Git commit or branch if the current working tree is not already safely backed up.

## Python

* Use modern, readable Python syntax appropriate for the project's Python version.
* Prefer standard library solutions when they are sufficient.
* Keep functions reasonably small and focused.
* Avoid unnecessary one-line constructions or overly clever code.
* Preserve existing behavior unless a change is explicitly requested.
* When modifying statistical code, pay particular attention to whether a code change could alter the statistical meaning or results.

## Data analysis

* Never silently change data, variable definitions, categories, missing-value handling, or statistical methods.
* When modifying analysis code, clearly distinguish between:

  * code/style improvements,
  * bug fixes,
  * and changes that may alter analytical results.
* Do not replace an existing statistical method with another method merely because it is newer or more fashionable. Explain the methodological difference first.

## Workflow

For substantial tasks, follow this sequence:

1. Inspect and understand the relevant code.
2. Describe the proposed approach.
3. Wait for confirmation if the change is potentially consequential.
4. Implement the agreed changes.
5. Review the resulting code for errors and unintended changes.
6. Summarize exactly what was changed.
7. If appropriate, suggest a simple test to verify that the original functionality is preserved.
