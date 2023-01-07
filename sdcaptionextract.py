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
        target_text = target_line[target_line.index("'", target_line.index("'", target_line.index("'") + 1) + 1) + 1:]  
        target_text = re.split(r"\\", target_text)[0]
        metadata.append((filename, target_text))

# Create a .txt file for each .PNG file with the same name as the .PNG file and the extracted text as its content
for filename, target_text in tqdm(metadata):
  with open(os.path.join(input_folder, filename[:-3] + 'txt'), 'w') as f:
    f.write(target_text)

print(f'Created .txt files for {len(metadata)} .PNG files')
print(f'Ignored {ignored_files} files')
