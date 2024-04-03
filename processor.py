import json
import markdown2

def apply_diff(original_content, diff_block):
    # Initialize a list to hold the final content
    final_content = []
    # Split the original content into lines
    original_lines = original_content.split('\n')
    # Use a set for faster lookup
    lines_to_remove = set()

    # First pass: mark lines to remove and add new lines immediately
    for line in diff_block.split('\n'):
        if line.startswith('+'):
            final_content.append(line[1:].strip())
        elif line.startswith('-'):
            lines_to_remove.add(line[1:].strip())

    # Second pass: add original lines that weren't marked for removal
    for line in original_lines:
        if line not in lines_to_remove:
            final_content.append(line)

    # Join the final content into a single string
    return '\n'.join(final_content)




def extract_code_blocks(markdown_text):
    # Convert markdown to HTML with fenced-code-blocks support
    html = markdown2.markdown(markdown_text, extras=["fenced-code-blocks"])
    
    # Initialize a list to hold code blocks
    code_blocks = []
    
    # Split the HTML content by lines to process each line
    lines = html.split('\n')
    inside_code_block = False
    current_code_block = []

    for line in lines:
        if line.startswith('<pre><code'):
            inside_code_block = True
            current_code_block = [line.replace('<pre><code>', '')]
        elif line.endswith('</code></pre>'):
            inside_code_block = False
            # Trim leading and trailing line breaks and append the cleaned code block
            last_line = line.replace('</code></pre>', '').strip()
            if len(last_line) >0:
                current_code_block.append(last_line)
            code_blocks.append(current_code_block)
            current_code_block = []
        elif inside_code_block:
            current_code_block.append(line)

    return code_blocks

try:
    with open("copilot.body", 'r') as file:
        http_response_content = file.read()

    data_chunks = http_response_content.split('data: ')[1:]
    delta_text = ''

    for chunk in data_chunks:
        try:
            json_data = json.loads(chunk)
            delta_text += extract_and_preserve_structure(json_data)
        except json.JSONDecodeError:
            # Optionally log or handle the error here
            pass

    # Use or print delta_text as needed
    # Save it to file
    with open("delta_text.txt", 'w') as file:
        file.write(delta_text)
    
    # print(delta_text)

    

    # Your markdown content (replace 'delta_text' with your actual markdown content variable)
    markdown_content = delta_text

    # Extract code blocks
    code_blocks = extract_code_blocks(markdown_content)

    #print("Code Blocks", code_blocks)

    original_content = """import logging

ap, ndcg = run_lambdamart(best_hyperparameter, save=True)

print("Finished with Metrics", ap, ndcg)
"""

    applied_diff = apply_diff(original_content, '\n'.join(code_blocks[0]))
    print(applied_diff)

except FileNotFoundError:
    print("The file copilot.body was not found.")
