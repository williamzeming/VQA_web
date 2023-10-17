import re

text = "The Inferred Mineral Resource of the Kalpini Project is estimated to be 76.4 million tonnes grading 0.73% Ni and 0.044% Co at a 0.5% Ni bottom cut-off grade. ##Sources: [Page number: 3, Section: EXECUTIVE SUMMARY]##"


pattern = re.compile(r'Sources: (\[.*?\])')
# Extracting "Sources:" content
source_content = re.findall(pattern, text)[0]
# Getting content outside the "Sources:" pattern
remaining_content = re.split(pattern, text)[0].strip()

result = remaining_content+"Sources: " +source_content
print(result)

##Where is the Kalpini Project located in relation to Kalgoorlie?
##What is the Inferred Mineral Resource of the Kalpini Project?