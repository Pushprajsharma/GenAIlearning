from bs4 import BeautifulSoup

# Read the HTML content from the file
with open('response.txt', 'rb') as file:
    content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Extract reviews (assuming reviews are in 'td.titleColumn a' for demonstration)
print (soup.select)

# Print the extracted reviews
for review in reviews:
    print(f"Review: {review}")
