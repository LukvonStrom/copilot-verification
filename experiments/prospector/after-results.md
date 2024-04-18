# Completion Verifier Output

| Tool | Passed Before Completion | Passed After Completion |
|---|---|---|
| Prospector (Code Quality) | ❌ | ❌ |
| Crosshair (Symbolic Execution) | ✅ | ✅ |

## Prospector Output
### Before Completion

| Code | Line | Message | Source |
| ---- | ---- | ------- | ------ |
| error | 34 | Name "x" is not defined  [name-defined] | mypy |
| singleton-comparison | 13 | Comparison 'self.data == None' should be 'self.data is None' | pylint |
| bare-except | 24 | No exception type(s) specified | pylint |
| E305 | 30 | expected 2 blank lines after class or function definition, found 1 | pycodestyle |
| unused-import | 1 | Unused import sys | pylint |
| bad-indentation | 4 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 5 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 6 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| unused-function | 21 | Unused function 'error_prone_function' | vulture |
| unused-function | 18 | Unused function 'unused_function' | vulture |


``` 
{
  "messages": [
    {
      "code": "error",
      "location": {
        "character": 11,
        "function": null,
        "line": 34,
        "module": null,
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Name \"x\" is not defined  [name-defined]",
      "source": "mypy"
    },
    {
      "code": "singleton-comparison",
      "location": {
        "character": 12,
        "function": "myClass.do_something",
        "line": 13,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Comparison 'self.data == None' should be 'self.data is None'",
      "source": "pylint"
    },
    {
      "code": "bare-except",
      "location": {
        "character": 4,
        "function": "error_prone_function",
        "line": 24,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "No exception type(s) specified",
      "source": "pylint"
    },
    {
      "code": "E305",
      "location": {
        "character": 1,
        "function": null,
        "line": 30,
        "module": null,
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "expected 2 blank lines after class or function definition, found 1",
      "source": "pycodestyle"
    },
    {
      "code": "unused-import",
      "location": {
        "character": 0,
        "function": null,
        "line": 1,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Unused import sys",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 4,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 5,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 6,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "unused-function",
      "location": {
        "character": null,
        "function": null,
        "line": 21,
        "module": null,
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Unused function 'error_prone_function'",
      "source": "vulture"
    },
    {
      "code": "unused-function",
      "location": {
        "character": null,
        "function": null,
        "line": 18,
        "module": null,
        "path": "uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Unused function 'unused_function'",
      "source": "vulture"
    }
  ],
  "summary": {
    "completed": "2024-04-18 14:06:43.035426",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 10,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 14:06:35.813695",
    "strictness": "from profile",
    "time_taken": "7.22",
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
| error | 36 | Name "x" is not defined  [name-defined] | mypy |
| singleton-comparison | 13 | Comparison 'self.data == None' should be 'self.data is None' | pylint |
| bare-except | 24 | No exception type(s) specified | pylint |
| E305 | 32 | expected 2 blank lines after class or function definition, found 1 | pycodestyle |
| unused-import | 1 | Unused import sys | pylint |
| bad-indentation | 4 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 5 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| bad-indentation | 6 | Bad indentation. Found 2 spaces, expected 4 | pylint |
| unused-function | 21 | Unused function 'error_prone_function' | vulture |
| unused-function | 18 | Unused function 'unused_function' | vulture |


```
{
  "messages": [
    {
      "code": "error",
      "location": {
        "character": 11,
        "function": null,
        "line": 36,
        "module": null,
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Name \"x\" is not defined  [name-defined]",
      "source": "mypy"
    },
    {
      "code": "singleton-comparison",
      "location": {
        "character": 12,
        "function": "myClass.do_something",
        "line": 13,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Comparison 'self.data == None' should be 'self.data is None'",
      "source": "pylint"
    },
    {
      "code": "bare-except",
      "location": {
        "character": 4,
        "function": "error_prone_function",
        "line": 24,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "No exception type(s) specified",
      "source": "pylint"
    },
    {
      "code": "E305",
      "location": {
        "character": 1,
        "function": null,
        "line": 32,
        "module": null,
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "expected 2 blank lines after class or function definition, found 1",
      "source": "pycodestyle"
    },
    {
      "code": "unused-import",
      "location": {
        "character": 0,
        "function": null,
        "line": 1,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Unused import sys",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 4,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 5,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "bad-indentation",
      "location": {
        "character": 0,
        "function": null,
        "line": 6,
        "module": "921370d5-4764-4000-aa90-aaf99bb5442b",
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Bad indentation. Found 2 spaces, expected 4",
      "source": "pylint"
    },
    {
      "code": "unused-function",
      "location": {
        "character": null,
        "function": null,
        "line": 21,
        "module": null,
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Unused function 'error_prone_function'",
      "source": "vulture"
    },
    {
      "code": "unused-function",
      "location": {
        "character": null,
        "function": null,
        "line": 18,
        "module": null,
        "path": "augmented-uploads/921370d5-4764-4000-aa90-aaf99bb5442b.py"
      },
      "message": "Unused function 'unused_function'",
      "source": "vulture"
    }
  ],
  "summary": {
    "completed": "2024-04-18 14:06:58.266732",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 10,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 14:06:50.589488",
    "strictness": "from profile",
    "time_taken": "7.68",
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

Session ID: `921370d5-4764-4000-aa90-aaf99bb5442b`

Time taken: 30.48 seconds
