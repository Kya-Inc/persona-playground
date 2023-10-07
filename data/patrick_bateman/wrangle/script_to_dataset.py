import re
import pandas as pd

# Read the script
with open('american_psycho.txt', 'r') as file:
    script = file.read()

# Split the script into chunks based on double newlines
chunks = re.split('\n\n', script)

# Initialize an empty list to store the dialogues
dialogues = []

# Iterate over the chunks
for chunk in chunks:
    # Split the chunk into lines
    lines = chunk.split('\n')
    # If the first line is a character name
    if re.match(r'^[A-Z\s]+(\s\(V\.O\.\))?$', lines[0]):
        # The rest of the lines are the dialogue
        dialogue = ' '.join(line for line in lines[1:] if not re.match(r'\(.*\)', line))
        dialogues.append((lines[0].strip(), dialogue.strip().strip('"')))
# Convert the list of dialogues into a DataFrame
df = pd.DataFrame(dialogues, columns=['character', 'line'])

# Save the DataFrame to a CSV file
df.to_csv('american_psycho.csv', index=False, quoting=3,sep="‚",escapechar="‚")