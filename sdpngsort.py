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

# Modify this regular expression to match the model name up until the next ','
model_re = re.compile(r'Model: (.*?),')
model_hash_re = re.compile(r'Model hash: (\w+)')
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
      model_match = model_re.search(metadata_str)
      if model_match:
        model = model_match.group(1)
      else:
        model_hash_match = model_hash_re.search(metadata_str)
        if model_hash_match:
          model = model_hash_match.group(1)
        else:
          ignored_files += 1
          continue
      metadata.append((filename, model))

files_by_model = defaultdict(list)
for filename, model in metadata:
  files_by_model[model].append(filename)

moved_files = 0
ignored_files_model = 0
for model, filenames in tqdm(files_by_model.items()):
  model_folder = os.path.join(input_folder, model)

  # Create the model folder if it does not exist
  if not os.path.exists(model_folder):
    os.makedirs(model_folder)

  # Move the image and text files to the model folder
  for filename in filenames:
    src_path = os.path.join(input_folder, filename)
    dst_path = os.path.join(model_folder, filename)
    try:
      os.rename(src_path, dst_path)
      moved_files += 1
    except FileExistsError:
      ignored_files_model += 1
      continue
    txt_src_path = src_path[:-3] + 'txt'
    txt_dst_path = dst_path[:-3] + 'txt'
    if os.path.exists(txt_src_path):
      os.rename(txt_src_path, txt_dst_path)

print(f'Moved {moved_files} files')
print(f'Ignored {ignored_files_model} files')
