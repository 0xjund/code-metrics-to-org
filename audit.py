import subprocess
import os
from auditor_parser import extract_sections, write_to_org, clean_output,remove_pre_content_lines

# Find all the .sol files in the current directory
sol_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".sol"):
            sol_files.append(os.path.join(root,file))

# Exit early if no files are found
if not sol_files:
    print("No solidity files found.")
    exit()

#Run the solidity metrics command
result = subprocess.run(
    ["solidity-code-metrics", *sol_files],
    capture_output = True,
    text = True
)
output = result.stdout
# remove precontent
output = remove_pre_content_lines(output)
# Clean and extract
cleaned_output = clean_output(output)
sections = extract_sections(output)

# Save it to audit.org
with open("audit.org", "w") as f:
    f.write("* Solidity Metrics Report\n\n")
    f.write("#+BEGIN_SRC text\n")
    f.write(cleaned_output)
    f.write("\n#+END_SRC\n")
