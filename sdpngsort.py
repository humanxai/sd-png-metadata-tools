import os
import re
import argparse
from collections import defaultdict
from tqdm import tqdm
from PIL import Image

# Maximum number of pixels allowed in an image
MAX_PIXELS = 128 * 1000000

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('input_folder', type=str, help='input folder')
parser.add_argument('-f', '--force', action='store_true', help='force overwrite of duplicate files')
args = parser.parse_args()

input_folder = args.input_folder
force_overwrite = args.force

# Compile regular expressions
model_re = re.compile(r'Model: (.*?),')
model_hash_re = re.compile(r'Model hash: (\w+)')

# Extract metadata from image files
metadata = []
for filename in tqdm(os.listdir(input_folder)):
  if filename.endswith('.png'):
    with Image.open(os.path.join(input_folder, filename)) as im:
      width, height = im.size
      if width * height > MAX_PIXELS:
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

# Group files by model
files_by_model = defaultdict(list)
for filename, model in metadata:
  files_by_model[model].append(filename)

# Move files to model folders
moved_files = 0
ignored_files_model = 0
for model, filenames in tqdm(files_by_model.items()):
  model_folder = os.path.join(input_folder, model)
  if not os.path.exists(model_folder):
    os.makedirs(model_folder)
  for filename in filenames:
    src_path = os.path.join(input_folder, filename)
    dst_path = os.path.join(model_folder, filename)
    if force_overwrite:
      os.replace(src_path, dst_path)
      moved_files += 1
    else:
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
