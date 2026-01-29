"""AI-powered code analysis and refactoring suggestions using LLM APIs."""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RefactoringSuggestion:
    """Represents an AI-generated refactoring suggestion."""
    title: str
    reasoning: str
    code_before: str
    code_after: str
    category: str
    priority: str


class AIAnalyzer:
    """AI-powered code analyzer using LLM APIs."""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "mock"):
        """Initialize the AI analyzer.
        
        Args:
            api_key: API key for the LLM provider (optional)
            provider: LLM provider to use ("openai", "anthropic", or "mock")
        """
        self.api_key = api_key or os.environ.get("LLM_API_KEY")
        self.provider = provider
        
        # Initialize provider if API key is available
        if self.provider == "openai" and self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                self.provider = "mock"
        elif self.provider == "anthropic" and self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                self.provider = "mock"
        else:
            self.provider = "mock"
    
    def suggest_refactorings(
        self, 
        source_code: str, 
        issues: List[Dict[str, Any]]
    ) -> List[RefactoringSuggestion]:
        """Generate AI-powered refactoring suggestions.
        
        Args:
            source_code: Python source code to analyze
            issues: List of detected code issues
            
        Returns:
            List of refactoring suggestions
        """
        if self.provider == "mock":
            return self._mock_suggestions(source_code, issues)
        elif self.provider == "openai":
            return self._openai_suggestions(source_code, issues)
        elif self.provider == "anthropic":
            return self._anthropic_suggestions(source_code, issues)
        else:
            return []
    
    def _mock_suggestions(
        self, 
        source_code: str, 
        issues: List[Dict[str, Any]]
    ) -> List[RefactoringSuggestion]:
        """Generate mock refactoring suggestions for testing.
        
        Args:
            source_code: Python source code to analyze
            issues: List of detected code issues
            
        Returns:
            List of mock refactoring suggestions
        """
        suggestions = []
        
        # Generate suggestions based on detected issues
        for issue in issues:
            if issue["type"] == "too_many_parameters":
                suggestions.append(RefactoringSuggestion(
                    title="Refactor function with too many parameters",
                    reasoning=(
                        "Functions with many parameters are hard to understand and maintain. "
                        "Consider grouping related parameters into a configuration object or data class."
                    ),
                    code_before="def func(a, b, c, d, e, f): ...",
                    code_after=(
                        "@dataclass\n"
                        "class FuncConfig:\n"
                        "    a: int\n"
                        "    b: int\n"
                        "    c: int\n"
                        "    d: int\n"
                        "    e: int\n"
                        "    f: int\n"
                        "\n"
                        "def func(config: FuncConfig): ..."
                    ),
                    category="complexity",
                    priority="high"
                ))
            
            elif issue["type"] == "long_method":
                suggestions.append(RefactoringSuggestion(
                    title="Extract methods from long function",
                    reasoning=(
                        "Long functions are difficult to understand and test. "
                        "Break down the function into smaller, well-named helper functions "
                        "that each do one thing well."
                    ),
                    code_before="def long_function(): # 50+ lines",
                    code_after=(
                        "def long_function():\n"
                        "    step1_result = _perform_step1()\n"
                        "    step2_result = _perform_step2(step1_result)\n"
                        "    return _finalize(step2_result)\n"
                        "\n"
                        "def _perform_step1(): ...\n"
                        "def _perform_step2(data): ...\n"
                        "def _finalize(data): ..."
                    ),
                    category="readability",
                    priority="medium"
                ))
            
            elif issue["type"] == "deep_nesting":
                suggestions.append(RefactoringSuggestion(
                    title="Reduce nesting depth with early returns",
                    reasoning=(
                        "Deep nesting makes code hard to follow. "
                        "Use early returns, guard clauses, or extract nested blocks into separate functions."
                    ),
                    code_before=(
                        "def func(x):\n"
                        "    if condition1:\n"
                        "        if condition2:\n"
                        "            if condition3:\n"
                        "                return result"
                    ),
                    code_after=(
                        "def func(x):\n"
                        "    if not condition1:\n"
                        "        return None\n"
                        "    if not condition2:\n"
                        "        return None\n"
                        "    if not condition3:\n"
                        "        return None\n"
                        "    return result"
                    ),
                    category="readability",
                    priority="medium"
                ))
            
            elif issue["type"] == "unused_import":
                # Extract import name from message
                import_name = "module"
                if "'" in issue.get('message', ''):
                    parts = issue.get('message', '').split("'")
                    if len(parts) >= 2:
                        import_name = parts[1]
                
                suggestions.append(RefactoringSuggestion(
                    title="Remove unused imports",
                    reasoning=(
                        "Unused imports clutter the code and can slow down module loading. "
                        "They should be removed to keep the code clean."
                    ),
                    code_before=f"import {import_name}",
                    code_after="# Import removed",
                    category="cleanliness",
                    priority="low"
                ))
            
            elif issue["type"] == "duplicate_code":
                suggestions.append(RefactoringSuggestion(
                    title="Extract duplicate code into a function",
                    reasoning=(
                        "Duplicate code leads to maintenance issues. "
                        "Extract the duplicated logic into a reusable function."
                    ),
                    code_before="# Duplicate code blocks",
                    code_after=(
                        "def extracted_function():\n"
                        "    # Common logic here\n"
                        "    pass\n"
                        "\n"
                        "# Use extracted_function() in both places"
                    ),
                    category="maintainability",
                    priority="high"
                ))
        
        return suggestions
    
    def _openai_suggestions(
        self, 
        source_code: str, 
        issues: List[Dict[str, Any]]
    ) -> List[RefactoringSuggestion]:
        """Generate suggestions using OpenAI API.
        
        Args:
            source_code: Python source code to analyze
            issues: List of detected code issues
            
        Returns:
            List of AI-generated refactoring suggestions
        """
        try:
            # Prepare the prompt
            issues_text = "\n".join([
                f"- Line {issue['line']}: {issue['type']} - {issue['message']}"
                for issue in issues
            ])
            
            prompt = f"""Analyze the following Python code and suggest refactorings based on the detected issues.

Code:
```python
{source_code}
```

Detected Issues:
{issues_text}

Provide 3-5 specific, actionable refactoring suggestions in JSON format with the following structure:
[
  {{
    "title": "Brief title",
    "reasoning": "Why this refactoring is needed",
    "code_before": "Example of problematic code",
    "code_after": "Example of refactored code",
    "category": "complexity|readability|maintainability|cleanliness",
    "priority": "high|medium|low"
  }}
]
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer specializing in Python refactoring."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse response
            content = response.choices[0].message.content
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            suggestions_data = json.loads(content)
            
            return [
                RefactoringSuggestion(**suggestion)
                for suggestion in suggestions_data
            ]
        
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._mock_suggestions(source_code, issues)
    
    def _anthropic_suggestions(
        self, 
        source_code: str, 
        issues: List[Dict[str, Any]]
    ) -> List[RefactoringSuggestion]:
        """Generate suggestions using Anthropic Claude API.
        
        Args:
            source_code: Python source code to analyze
            issues: List of detected code issues
            
        Returns:
            List of AI-generated refactoring suggestions
        """
        try:
            # Prepare the prompt
            issues_text = "\n".join([
                f"- Line {issue['line']}: {issue['type']} - {issue['message']}"
                for issue in issues
            ])
            
            prompt = f"""Analyze the following Python code and suggest refactorings based on the detected issues.

Code:
```python
{source_code}
```

Detected Issues:
{issues_text}

Provide 3-5 specific, actionable refactoring suggestions in JSON format with the following structure:
[
  {{
    "title": "Brief title",
    "reasoning": "Why this refactoring is needed",
    "code_before": "Example of problematic code",
    "code_after": "Example of refactored code",
    "category": "complexity|readability|maintainability|cleanliness",
    "priority": "high|medium|low"
  }}
]
"""
            
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse response
            content = message.content[0].text
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            suggestions_data = json.loads(content)
            
            return [
                RefactoringSuggestion(**suggestion)
                for suggestion in suggestions_data
            ]
        
        except Exception as e:
            print(f"Error calling Anthropic API: {e}")
            return self._mock_suggestions(source_code, issues)
