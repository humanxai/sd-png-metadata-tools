import os
import re
from collections import defaultdict
from tqdm import tqdm
from PIL import Image

# Maximum number of pixels allowed in an image
MAX_PIXELS = 128 * 1000000

input_folder = input('Enter the path to the input folder (leave blank for current directory): ')
if not input_folder:
  input_folder = os.getcwd()

# Modify this regular expression to match the model name up until the next ','
model_re = re.compile(r'Model: (.*?),')
model_hash_re = re.compile(r'Model hash: (\w+)')
metadata = []
for filename in tqdm(os.listdir(input_folder)):
  if filename.endswith('.png'):
    # Open the image file with PIL.Image.File
    with Image.open(os.path.join(input_folder, filename)) as im:
      # Check the size of the image
      width, height = im.size
      if width * height > MAX_PIXELS:
        # Skip images that are too large
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
          continue
      metadata.append((filename, model))

files_by_model = defaultdict(list)
for filename, model in metadata:
  files_by_model[model].append(filename)

for model, filenames in tqdm(files_by_model.items()):
  model_folder = os.path.join(input_folder, model)

# Create the model folder if it does not exist
  if not os.path.exists(model_folder):
    os.makedirs(model_folder)

# Move the image and text files to the model folder
  for filename in filenames:
    src_path = os.path.join(input_folder, filename)
    dst_path = os.path.join(model_folder, filename)
    os.rename(src_path, dst_path)
    txt_src_path = src_path[:-3] + 'txt'
    txt_dst_path = dst_path[:-3] + 'txt'
    if os.path.exists(txt_src_path):
      os.rename(txt_src_path, txt_dst_path)
