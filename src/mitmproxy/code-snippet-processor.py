import json
import markdown2


def apply_diff(original_content, diff_block):
    # Initialize a list to hold the final content
    final_content = []
    # Split the original content into lines
    original_lines = original_content.split("\n")
    # Use a set for faster lookup
    lines_to_remove = set()

    # First pass: mark lines to remove and add new lines immediately
    for line in diff_block.split("\n"):
        if line.startswith("+"):
            final_content.append(line[1:].strip())
        elif line.startswith("-"):
            lines_to_remove.add(line[1:].strip())

    # Second pass: add original lines that weren't marked for removal
    for line in original_lines:
        if line not in lines_to_remove:
            final_content.append(line)

    # Join the final content into a single string
    return "\n".join(final_content)


def extract_code_blocks(markdown_text):
    # Convert markdown to HTML with fenced-code-blocks support
    html = markdown2.markdown(markdown_text, extras=["fenced-code-blocks"])

    # Initialize a list to hold code blocks
    code_blocks = []

    # Split the HTML content by lines to process each line
    lines = html.split("\n")
    inside_code_block = False
    current_code_block = []

    for line in lines:
        if line.startswith("<pre><code"):
            inside_code_block = True
            current_code_block = [line.replace("<pre><code>", "")]
        elif line.endswith("</code></pre>"):
            inside_code_block = False
            # Trim leading and trailing line breaks and append the cleaned code block
            last_line = line.replace("</code></pre>", "").strip()
            if len(last_line) > 0:
                current_code_block.append(last_line)
            code_blocks.append(current_code_block)
            current_code_block = []
        elif inside_code_block:
            current_code_block.append(line)

    return code_blocks

    # Extract code blocks
    code_blocks = extract_code_blocks(markdown_content)

    final_content = None

    # if present split of # FILEPATH # BEGIN and #END until respective end of line from original_content
    if "# BEGIN" in original_content:
        # get the line for each
        original_content = original_content.split("\n")
        # get the index of the line
        begin_index = original_content.index("# BEGIN")
        end_index = original_content.index("# END")
        filepath_index = original_content.index("# FILEPATH")
        # remove them from list
        del original_content[begin_index]
        del original_content[end_index]
        del original_content[filepath_index]
        # join the list back to string
        final_content = "\n".join(original_content)
    else:
        # Its a diff for longer contents
        final_content = apply_diff(original_content, "\n".join(code_blocks[0]))
