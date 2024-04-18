# Completion Verifier Output

| Tool | Passed Before Completion | Passed After Completion |
|---|---|---|
| Prospector (Code Quality) | ❌ | ❌ |
| Crosshair (Symbolic Execution) | ✅ | ✅ |

## Prospector Output
### Before Completion

| Code | Line | Message | Source |
| ---- | ---- | ------- | ------ |
| E305 | 31 | expected 2 blank lines after class or function definition, found 1 | pycodestyle |
| reportOptionalMemberAccess | 7 | "get" is not a known member of "None" | pyright |
| unused-function | 5 | Unused function 'process_data' | vulture |


``` 
{
  "messages": [
    {
      "code": "E305",
      "location": {
        "character": 1,
        "function": null,
        "line": 31,
        "module": null,
        "path": "uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "expected 2 blank lines after class or function definition, found 1",
      "source": "pycodestyle"
    },
    {
      "code": "reportOptionalMemberAccess",
      "location": {
        "character": 30,
        "function": null,
        "line": 7,
        "module": null,
        "path": "uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "\"get\" is not a known member of \"None\"",
      "source": "pyright"
    },
    {
      "code": "unused-function",
      "location": {
        "character": null,
        "function": null,
        "line": 5,
        "module": null,
        "path": "uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Unused function 'process_data'",
      "source": "vulture"
    }
  ],
  "summary": {
    "completed": "2024-04-18 13:37:56.238170",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 3,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 13:37:06.644900",
    "strictness": "from profile",
    "time_taken": "49.59",
    "tools": [
      "dodgy",
      "mccabe",
      "mypy",
      "profile-validator",
      "pycodestyle",
      "pyflakes",
      "pylint",
      "pyright",
      "vulture"
    ]
  }
}
```
### After Completion
| Code | Line | Message | Source |
| ---- | ---- | ------- | ------ |
| E114 | 7 | indentation is not a multiple of 4 (comment) | pycodestyle |
| reportOptionalMemberAccess | 7 | "get" is not a known member of "None" | pyright |
| E114 | 10 | indentation is not a multiple of 4 (comment) | pycodestyle |
| E114 | 13 | indentation is not a multiple of 4 (comment) | pycodestyle |
| E114 | 19 | indentation is not a multiple of 4 (comment) | pycodestyle |
| E114 | 26 | indentation is not a multiple of 4 (comment) | pycodestyle |
| E305 | 31 | expected 2 blank lines after class or function definition, found 1 | pycodestyle |
| bad-indentation | 8 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 11 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 14 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 15 | Bad indentation. Found 4 spaces, expected 8 | pylint |
| bad-indentation | 16 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 17 | Bad indentation. Found 4 spaces, expected 8 | pylint |
| bad-indentation | 20 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 21 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 22 | Bad indentation. Found 4 spaces, expected 8 | pylint |
| bad-indentation | 23 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 24 | Bad indentation. Found 4 spaces, expected 8 | pylint |
| bad-indentation | 27 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 29 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| unused-function | 5 | Unused function 'calculate' | vulture |


```
{
  "messages": [
    {
      "code": "E114",
      "location": {
        "character": 3,
        "function": null,
        "line": 7,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "indentation is not a multiple of 4 (comment)",
      "source": "pycodestyle"
    },
    {
      "code": "reportOptionalMemberAccess",
      "location": {
        "character": 28,
        "function": null,
        "line": 7,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "\"get\" is not a known member of \"None\"",
      "source": "pyright"
    },
    {
      "code": "E114",
      "location": {
        "character": 3,
        "function": null,
        "line": 10,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "indentation is not a multiple of 4 (comment)",
      "source": "pycodestyle"
    },
    {
      "code": "E114",
      "location": {
        "character": 3,
        "function": null,
        "line": 13,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "indentation is not a multiple of 4 (comment)",
      "source": "pycodestyle"
    },
    {
      "code": "E114",
      "location": {
        "character": 3,
        "function": null,
        "line": 19,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "indentation is not a multiple of 4 (comment)",
      "source": "pycodestyle"
    },
    {
      "code": "E114",
      "location": {
        "character": 3,
        "function": null,
        "line": 26,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "indentation is not a multiple of 4 (comment)",
      "source": "pycodestyle"
    },
    {
      "code": "E305",
      "location": {
        "character": 1,
        "function": null,
        "line": 31,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "expected 2 blank lines after class or function definition, found 1",
      "source": "pycodestyle"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 8,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 11,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 14,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 15,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 4 spaces, expected 8",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 16,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 17,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 4 spaces, expected 8",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 20,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 21,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 22,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 4 spaces, expected 8",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 23,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 24,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 4 spaces, expected 8",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 27,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 29,
        "module": "66ff7a5a-e99c-4117-9e00-0c6642841e8a",
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "unused-function",
      "location": {
        "character": null,
        "function": null,
        "line": 5,
        "module": null,
        "path": "augmented-uploads/66ff7a5a-e99c-4117-9e00-0c6642841e8a.py"
      },
      "message": "Unused function 'calculate'",
      "source": "vulture"
    }
  ],
  "summary": {
    "completed": "2024-04-18 13:38:31.886931",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 21,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 13:38:07.111959",
    "strictness": "from profile",
    "time_taken": "24.77",
    "tools": [
      "dodgy",
      "mccabe",
      "mypy",
      "profile-validator",
      "pycodestyle",
      "pyflakes",
      "pylint",
      "pyright",
      "vulture"
    ]
  }
}
```

## Crosshair Output
### Before Completion
```
null
```
### After Completion
```
null
```

--- 

Session ID: `66ff7a5a-e99c-4117-9e00-0c6642841e8a`

Time taken: 94.88 seconds
