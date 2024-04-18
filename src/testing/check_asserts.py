import ast
import json
import os


class AssertVisitor(ast.NodeVisitor):
    def __init__(self, file_uri, content):
        self.diagnostics = []
        self.file_uri = file_uri

    def visit_FunctionDef(self, node):
        # Count assert statements within this function
        assert_count = sum(1 for _ in ast.walk(node) if isinstance(_, ast.Assert))
        if assert_count < 2:
            # If less than two asserts, create a diagnostic message

            diagnostic = {
                "range": {
                    "start": {"line": node.lineno - 1, "character": node.col_offset},
                    "end": {
                        "line": node.lineno - 1,
                        "character": node.end_col_offset - 2,
                    },
                },
                "severity": 0,
                "code": "assert-check",
                "source": "AssertCheck",
                "message": f"Function '{node.name}' does not have at least two assert statements (pre- and postcondition) needed for CrossHair symbolic execution of this method. Come up with sensible pre- and postconditions and add them as assert statements in the function body. For more information, see https://crosshair.readthedocs.io/en/latest/kinds_of_contracts.html#assert-based-contracts.",
            }
            self.diagnostics.append(diagnostic)
        self.generic_visit(node)

    def get_final_diagnostics(self):
        return {
            "method": "textDocument/publishDiagnostics",
            "params": {"uri": self.file_uri, "diagnostics": self.diagnostics},
        }


def check_asserts(file_path_or_content, file_path=None):
    try:
        if os.path.exists(file_path_or_content):
            with open(file_path_or_content, "r", encoding="utf-8") as file:
                content = file.read()
            file_uri = f"file://{file_path_or_content}"
        else:
            content = file_path_or_content
            file_uri = file_path

        visitor = AssertVisitor(file_uri, content)
        visitor.visit(ast.parse(content))
        return visitor.get_final_diagnostics()
    except Exception as e:
        return
