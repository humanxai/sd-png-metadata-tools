# sd-png-metadata-tools
A collection of tools pertaining to .PNG files created but automatic1111's Stable Diffusion WebUI.




# sd-png-sort
Sorts folders containing PNG images produced by stable diffusion automatic1111 webui into subfolders according to modelname or modelhash in metadata.

To use this script, you can run it from the command line like this:

python sdpngsort.py /path/to/input/folder

If you do not provide a path, it will default to the current working directory.

# sd-caption-extract
Extracts the prompt from .png files and places them into a similarly named .txt files 

To use this script, you can run it from the command line like this:

python sdcaptionextract /path/to/input/folder

If you do not provide a path, it will default to the current working directory.

# sd-mega-caption

Extracts the prompt from .png files and places them into a single .txt file called Output.txt
Avoids duplicates.

To use this script, you can run it from the command line like this:

python sdmegacaption.py /path/to/input/folder

If you do not provide a path, it will default to the current working directory.
