# Completion Verifier Output

| Tool | Passed Before Completion | Passed After Completion |
|---|---|---|
| Prospector (Code Quality) | ❌ | ❌ |
| Crosshair (Symbolic Execution) | ❌ | ❌ |

## Prospector Output
### Before Completion

| Code | Line | Message | Source |
| ---- | ---- | ------- | ------ |
| consider-using-dict-items | 30 | Consider iterating with .items() | pylint |


``` 
{
  "messages": [
    {
      "code": "consider-using-dict-items",
      "location": {
        "character": 0,
        "function": "ShoppingCart.calculate_total_price",
        "line": 30,
        "module": "909085b2-b90d-4804-b9f0-4c408c4a1da4",
        "path": "uploads/909085b2-b90d-4804-b9f0-4c408c4a1da4.py"
      },
      "message": "Consider iterating with .items()",
      "source": "pylint"
    }
  ],
  "summary": {
    "completed": "2024-04-18 13:54:22.789444",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 1,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 13:54:13.791780",
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
### After Completion
| Code | Line | Message | Source |
| ---- | ---- | ------- | ------ |
| error | 32 | Name "calculate_total_price" already defined on line 25  [no-redef] | mypy |
| E305 | 40 | expected 2 blank lines after class or function definition, found 1 | pycodestyle |
| F811 | 32 | redefinition of unused 'calculate_total_price' from line 25 | pyflakes |
| consider-using-dict-items | 30 | Consider iterating with .items() | pylint |
| consider-using-dict-items | 37 | Consider iterating with .items() | pylint |
| reportRedeclaration | 24 | Method declaration "calculate_total_price" is obscured by a declaration of the same name | pyright |


```
{
  "messages": [
    {
      "code": "error",
      "location": {
        "character": 5,
        "function": null,
        "line": 32,
        "module": null,
        "path": "augmented-uploads/909085b2-b90d-4804-b9f0-4c408c4a1da4.py"
      },
      "message": "Name \"calculate_total_price\" already defined on line 25  [no-redef]",
      "source": "mypy"
    },
    {
      "code": "E305",
      "location": {
        "character": 1,
        "function": null,
        "line": 40,
        "module": null,
        "path": "augmented-uploads/909085b2-b90d-4804-b9f0-4c408c4a1da4.py"
      },
      "message": "expected 2 blank lines after class or function definition, found 1",
      "source": "pycodestyle"
    },
    {
      "code": "F811",
      "location": {
        "character": 5,
        "function": null,
        "line": 32,
        "module": null,
        "path": "augmented-uploads/909085b2-b90d-4804-b9f0-4c408c4a1da4.py"
      },
      "message": "redefinition of unused 'calculate_total_price' from line 25",
      "source": "pyflakes"
    },
    {
      "code": "consider-using-dict-items",
      "location": {
        "character": 0,
        "function": "ShoppingCart.calculate_total_price",
        "line": 30,
        "module": "909085b2-b90d-4804-b9f0-4c408c4a1da4",
        "path": "augmented-uploads/909085b2-b90d-4804-b9f0-4c408c4a1da4.py"
      },
      "message": "Consider iterating with .items()",
      "source": "pylint"
    },
    {
      "code": "consider-using-dict-items",
      "location": {
        "character": 0,
        "function": "ShoppingCart.calculate_total_price",
        "line": 37,
        "module": "909085b2-b90d-4804-b9f0-4c408c4a1da4",
        "path": "augmented-uploads/909085b2-b90d-4804-b9f0-4c408c4a1da4.py"
      },
      "message": "Consider iterating with .items()",
      "source": "pylint"
    },
    {
      "code": "reportRedeclaration",
      "location": {
        "character": 8,
        "function": null,
        "line": 24,
        "module": null,
        "path": "augmented-uploads/909085b2-b90d-4804-b9f0-4c408c4a1da4.py"
      },
      "message": "Method declaration \"calculate_total_price\" is obscured by a declaration of the same name",
      "source": "pyright"
    }
  ],
  "summary": {
    "completed": "2024-04-18 13:54:42.807265",
    "formatter": "json",
    "libraries": [
      "flask"
    ],
    "message_count": 6,
    "profiles": "/usr/src/app/.prospector.yaml, default, no_member_warnings, no_doc_warnings, strictness_medium, strictness_high, strictness_veryhigh",
    "started": "2024-04-18 13:54:33.854855",
    "strictness": "from profile",
    "time_taken": "8.95",
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

Session ID: `909085b2-b90d-4804-b9f0-4c408c4a1da4`

Time taken: 39.89 seconds
