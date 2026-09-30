"""Extract the two original figure images from Power et al., arXiv:2201.02177v1.

Usage: python extract_grokking.py paper.pdf output_directory
Requires pypdf. Source: https://arxiv.org/pdf/2201.02177v1
Extracts the embedded images directly, without cropping or redrawing curves.
"""
from pathlib import Path
import sys
from pypdf import PdfReader

source, output = Path(sys.argv[1]), Path(sys.argv[2])
output.mkdir(parents=True, exist_ok=True)
reader = PdfReader(source)
# Figure 1 left (page 1), Figure 4 (page 7); exact image names in the v1 PDF.
for name, page_index, image_name in [('grokking-accuracy', 0, 'Im1.png'),
                                      ('grokking-loss', 6, 'Im8.png')]:
    matches = [i for i in reader.pages[page_index].images if i.name == image_name]
    if len(matches) != 1:
        raise ValueError(f'Expected one {image_name} on page {page_index + 1}')
    (output / (name + '.png')).write_bytes(matches[0].data)
