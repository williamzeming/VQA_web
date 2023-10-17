import re

text = "The project lease was owned by Anthony Warren Slater (‘AWS’). [Sources: Page number: 4, Section: 1. Introduction]"

pattern = re.compile(r'Sources: (\[.*?\])')
# Extracting "Sources:" content
source_content = re.findall(pattern, text)[0]
# Getting content outside the "Sources:" pattern
remaining_content = re.split(pattern, text)[0].strip()

result = remaining_content+"Sources: " +source_content
print(result)

##Where is the Kalpini Project located in relation to Kalgoorlie?
##What is the Inferred Mineral Resource of the Kalpini Project?