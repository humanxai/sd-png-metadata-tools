import os
import re
from collections import defaultdict
from tqdm import tqdm
from PIL import Image
import sys

# Maximum number of pixels allowed in an image
MAX_PIXELS = 128 * 1000000

# Check if an input folder was provided as a command-line argument
if len(sys.argv) > 1:
  input_folder = sys.argv[1]
else:
  input_folder = os.getcwd()

metadata = []
ignored_files = 0
for filename in tqdm(os.listdir(input_folder)):
  if filename.endswith('.png'):
    # Open the image file with PIL.Image.File
    with Image.open(os.path.join(input_folder, filename)) as im:
      # Check the size of the image
      width, height = im.size
      if width * height > MAX_PIXELS:
        # Skip images that are too large
        ignored_files += 1
        continue

      metadata_str = str(im.info)
      metadata_lines = metadata_str.splitlines()
      if len(metadata_lines) > 0:
        # Extract everything after the third "'" and up to the first "\n"
        target_line = metadata_lines[0]
        try:
              target_text = target_line[target_line.index("'", target_line.index("'", target_line.index("'") + 1) + 1) + 1:]
              target_text = re.split(r"\\", target_text)[0]
              metadata.append((filename, target_text))
        except ValueError:
              ignored_files += 1
            # Ignore .PNG files that do not have any metadata
        pass

metadata_set = set()

# Iterate over the metadata and add the extracted text to metadata_set
for _, target_text in tqdm(metadata):
  metadata_set.add(target_text)

# Open Output.txt in write mode
with open(os.path.join(input_folder, 'Output.txt'), 'w') as f:
  # Write the extracted text from the metadata of each .PNG file to Output.txt
  for target_text in metadata_set:
    f.write(target_text + '\n')

print(f'Created Output.txt containing the extracted text from the metadata of {len(metadata_set)} .PNG files')
print(f'Ignored {ignored_files} files')
