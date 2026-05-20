## Learning Progress

### Day 2 — Iteration Patterns (Loops)
**Concepts covered:**
- `for` loops over collections with real data
- `while` loops for retry logic and queue processing
- `range()`, `enumerate()`, `zip()` — professional iteration tools
- Loop control: `break`, `continue`, `for/else`

**Mini Project: Log Analyzer**
- Reads a server log file, classifies entries by level (INFO/WARNING/ERROR/DEBUG)
- Extracts and reports errors with an ASCII bar chart summary
- Structured with modular functions and `if __name__ == '__main__'` pattern
- Location: `mini_projects/log_analyzer/`

**Key engineering insight:** Loops are transformation pipelines over collections,
not just repetition tools. Every backend system and AI pipeline uses this pattern.