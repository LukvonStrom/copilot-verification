# Completion Verifier Output

| Tool | Passed Before Completion | Passed After Completion |
|---|---|---|
| Prospector (Code Quality) | ❌ | ❌ |
| Crosshair (Symbolic Execution) | ❌ | ❌ |

## Prospector Output
### Before Completion

| Code | Line | Message | Source |
| ---- | ---- | ------- | ------ |
| error | 46 | "ShoppingCart" has no attribute "get_total_price"  [attr-defined] | mypy |
| error | 52 | "ShoppingCart" has no attribute "get_total_price"  [attr-defined] | mypy |
| F841 | 22 | local variable 'e' is assigned to but never used | pyflakes |
| F841 | 31 | local variable 'e' is assigned to but never used | pyflakes |
| F841 | 36 | local variable 'e' is assigned to but never used | pyflakes |
| F841 | 47 | local variable 'e' is assigned to but never used | pyflakes |
| reportAttributeAccessIssue | 45 | Cannot access member "get_total_price" for type "ShoppingCart"   Member "get_total_price" is unknown | pyright |
| reportAttributeAccessIssue | 51 | Cannot access member "get_total_price" for type "ShoppingCart"   Member "get_total_price" is unknown | pyright |


``` 
{
  "messages": [
    {
      "code": "error",
      "location": {
        "character": 9,
        "function": null,
        "line": 46,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "\"ShoppingCart\" has no attribute \"get_total_price\"  [attr-defined]",
      "source": "mypy"
    },
    {
      "code": "error",
      "location": {
        "character": 19,
        "function": null,
        "line": 52,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "\"ShoppingCart\" has no attribute \"get_total_price\"  [attr-defined]",
      "source": "mypy"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 22,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 31,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 36,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 47,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "reportAttributeAccessIssue",
      "location": {
        "character": 13,
        "function": null,
        "line": 45,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "Cannot access member \"get_total_price\" for type \"ShoppingCart\"\n  Member \"get_total_price\" is unknown",
      "source": "pyright"
    },
    {
      "code": "reportAttributeAccessIssue",
      "location": {
        "character": 23,
        "function": null,
        "line": 51,
        "module": null,
        "path": "uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "Cannot access member \"get_total_price\" for type \"ShoppingCart\"\n  Member \"get_total_price\" is unknown",
      "source": "pyright"
    }
  ],
  "summary": {
    "completed": "2024-04-18 13:57:06.735135",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 8,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 13:56:57.840763",
    "strictness": "from profile",
    "time_taken": "8.89",
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
| error | 52 | "ShoppingCart" has no attribute "get_total_price"  [attr-defined] | mypy |
| error | 58 | "ShoppingCart" has no attribute "get_total_price"  [attr-defined] | mypy |
| E305 | 24 | expected 2 blank lines after class or function definition, found 1 | pycodestyle |
| F841 | 28 | local variable 'e' is assigned to but never used | pyflakes |
| F841 | 37 | local variable 'e' is assigned to but never used | pyflakes |
| F841 | 42 | local variable 'e' is assigned to but never used | pyflakes |
| F841 | 53 | local variable 'e' is assigned to but never used | pyflakes |
| reportAttributeAccessIssue | 51 | Cannot access member "get_total_price" for type "ShoppingCart"   Member "get_total_price" is unknown | pyright |
| reportAttributeAccessIssue | 57 | Cannot access member "get_total_price" for type "ShoppingCart"   Member "get_total_price" is unknown | pyright |


```
{
  "messages": [
    {
      "code": "error",
      "location": {
        "character": 9,
        "function": null,
        "line": 52,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "\"ShoppingCart\" has no attribute \"get_total_price\"  [attr-defined]",
      "source": "mypy"
    },
    {
      "code": "error",
      "location": {
        "character": 19,
        "function": null,
        "line": 58,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "\"ShoppingCart\" has no attribute \"get_total_price\"  [attr-defined]",
      "source": "mypy"
    },
    {
      "code": "E305",
      "location": {
        "character": 1,
        "function": null,
        "line": 24,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "expected 2 blank lines after class or function definition, found 1",
      "source": "pycodestyle"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 28,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 37,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 42,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "F841",
      "location": {
        "character": 5,
        "function": null,
        "line": 53,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "local variable 'e' is assigned to but never used",
      "source": "pyflakes"
    },
    {
      "code": "reportAttributeAccessIssue",
      "location": {
        "character": 13,
        "function": null,
        "line": 51,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "Cannot access member \"get_total_price\" for type \"ShoppingCart\"\n  Member \"get_total_price\" is unknown",
      "source": "pyright"
    },
    {
      "code": "reportAttributeAccessIssue",
      "location": {
        "character": 23,
        "function": null,
        "line": 57,
        "module": null,
        "path": "augmented-uploads/b2e89043-d5e0-4114-878e-d3dbb8d2a7ef.py"
      },
      "message": "Cannot access member \"get_total_price\" for type \"ShoppingCart\"\n  Member \"get_total_price\" is unknown",
      "source": "pyright"
    }
  ],
  "summary": {
    "completed": "2024-04-18 13:57:23.859832",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 9,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 13:57:14.864806",
    "strictness": "from profile",
    "time_taken": "9.00",
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
[
  {
    "line_number": "11",
    "message": "AssertionError Maximum item limit reached when calling add_item(ShoppingCart(1), '', 2)"
  }
]
```
### After Completion
```
[
  {
    "line_number": "11",
    "message": "AssertionError Maximum item limit reached when calling add_item(ShoppingCart(1), '', 2)"
  }
]
```

--- 

Session ID: `b2e89043-d5e0-4114-878e-d3dbb8d2a7ef`

Time taken: 35.01 seconds
