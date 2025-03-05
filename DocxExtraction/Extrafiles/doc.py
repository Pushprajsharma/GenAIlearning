import docx
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

def extract_requirements_and_tables(doc_path):
    # Load the document
    doc = docx.Document(doc_path)
    requirements = {}
    current_heading = None

    # Iterate through each element in the document's body
    for element in doc.element.body:
        if isinstance(element, CT_P):  # Paragraph
            para = docx.text.paragraph.Paragraph(element, doc)

            # Check if the paragraph is a heading containing "Requirements"
            if para.style.name.startswith('Heading') and "Requirements" in para.text:
                current_heading = para.text.strip()
                requirements[current_heading] = {
                    'text': [],
                    'tables': []
                }
            elif current_heading:
                # Add the paragraph to the current heading's text list
                text = para.text.strip()
                if text:
                    requirements[current_heading]['text'].append(text)
        elif isinstance(element, CT_Tbl):  # Table
            table = docx.table.Table(element, doc)
            if current_heading:
                # Add the table to the current heading's tables list
                table_data = []
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)
                requirements[current_heading]['tables'].append(table_data)

    # Remove headings without any text or tables
    requirements = {heading: content for heading, content in requirements.items() if content['text'] or content['tables']}
    
    return requirements

# Example usage
doc_path = "C:\\Users\\pushpraj.sharma\\Downloads\\DocxExtraction\\Sample URS_008 Content Manager.docx"
requirements = extract_requirements_and_tables(doc_path)

# Store extracted requirements and tables in a variable
output_content = ""
for heading, content in requirements.items():
    output_content += f"{heading}:\n"
    output_content += "  Text:\n"
    for text in content['text']:
        output_content += f"    - {text}\n"
    if content['tables']:  # Only add tables section if there are tables
        output_content += "  Tables:\n"
        for table in content['tables']:
            output_content += "    Table:\n"
            for row in table:
                output_content += f"      {row}\n"
    output_content += "\n" if content['text'] or content['tables'] else ""

# Now `output_content` contains the formatted requirements and tables

print(output_content)
