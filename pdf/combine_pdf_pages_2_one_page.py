# function: to combine part of the pdf horizontally to get a better view/comparison
# input: [filepath: input.pdf] [filepath: output.pdf] [list: pages you want to combine, use '-' to seperates]
# output: a combined pdf file

import os
from pypdf import PdfReader, PdfWriter, PageObject
from typing import List, Tuple

def parse_range(range_str: str) -> Tuple[int, int]:
    """
    Parses a range string (e.g., '2-4') and returns a tuple of zero-based indices.
    
    Parameters:
    - range_str: A string representing the range, e.g., '2-4'.
    
    Returns:
    - A tuple (start, end) with zero-based page indices.
    """
    parts = range_str.split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid range format: '{range_str}'. Expected format 'start-end'.")
    try:
        start = int(parts[0].strip()) - 1  # Convert to zero-based index
        end = int(parts[1].strip()) - 1
        if start > end:
            raise ValueError(f"Start page {start + 1} is greater than end page {end + 1} in range '{range_str}'.")
        return (start, end)
    except ValueError as ve:
        raise ValueError(f"Invalid numbers in range '{range_str}': {ve}")

def merge_pages_horizontally(pages: List[PageObject]) -> PageObject:
    """
    Merges a list of PyPDF PageObject pages horizontally into a single PageObject.
    
    Parameters:
    - pages: List of PageObject instances to merge.
    
    Returns:
    - A new PageObject with the merged content.
    """
    if not pages:
        raise ValueError("No pages to merge.")
    
    # Determine total width and maximum height
    total_width = sum(page.mediabox.width for page in pages)
    max_height = max(page.mediabox.height for page in pages)
    
    # Create a new blank page with the combined width and max height
    new_page = PageObject.create_blank_page(width=total_width, height=max_height)
    
    current_x = 0
    for page in pages:
        # Calculate y offset to align pages vertically (bottom-aligned)
        y_offset = 0  # Change if you want different vertical alignment
        # Merge the page onto the new page at the current x position
        new_page.merge_translated_page(page, current_x, y_offset)
        current_x += page.mediabox.width
    
    return new_page

def parse_ranges(ranges: List[str], total_pages: int) -> List[Tuple[int, int]]:
    """
    Parses a list of range strings and validates them against the total number of pages.
    
    Parameters:
    - ranges: List of range strings, e.g., ['2-4', '7-10'].
    - total_pages: Total number of pages in the PDF.
    
    Returns:
    - A list of tuples with zero-based start and end indices.
    """
    parsed_ranges = []
    for range_str in ranges:
        start, end = parse_range(range_str)
        if start < 0 or end >= total_pages:
            raise ValueError(f"Range '{range_str}' is out of bounds for a document with {total_pages} pages.")
        parsed_ranges.append((start, end))
    
    # Check for overlapping ranges
    sorted_ranges = sorted(parsed_ranges, key=lambda x: x[0])
    for i in range(1, len(sorted_ranges)):
        prev_end = sorted_ranges[i-1][1]
        current_start = sorted_ranges[i][0]
        if current_start <= prev_end:
            raise ValueError(f"Ranges '{sorted_ranges[i-1]}' and '{sorted_ranges[i]}' overlap.")
    
    return sorted_ranges

def reorganize_pdf(input_pdf_path: str, output_pdf_path: str, merge_ranges: List[str]):
    """
    Reorganizes the PDF by combining specified page ranges horizontally while preserving vector graphics.
    
    Parameters:
    - input_pdf_path: Path to the input PDF file.
    - output_pdf_path: Path where the output PDF will be saved.
    - merge_ranges: List of range strings to merge, e.g., ['2-4', '7-10'].
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    print(f"Total pages in input PDF: {total_pages}")
    
    # Parse and validate merge ranges
    try:
        parsed_ranges = parse_ranges(merge_ranges, total_pages)
    except ValueError as ve:
        print(f"Error parsing ranges: {ve}")
        return
    
    # Create a list to track pages that have been merged
    merged_pages = set()
    
    # Process each range and merge
    for start, end in parsed_ranges:
        # Add pages to merged_pages set
        for i in range(start, end + 1):
            merged_pages.add(i)
    
    # Iterate through all pages and add to writer
    current_page = 0
    while current_page < total_pages:
        if current_page in merged_pages:
            # Find which range this page belongs to
            for start, end in parsed_ranges:
                if start == current_page:
                    # Merge pages from start to end
                    pages_to_merge = [reader.pages[i] for i in range(start, end + 1)]
                    merged_page = merge_pages_horizontally(pages_to_merge)
                    writer.add_page(merged_page)
                    print(f"Merged pages {start + 1}-{end + 1} into a single page.")
                    current_page = end + 1  # Skip merged pages
                    break
        else:
            # Add the page as is
            writer.add_page(reader.pages[current_page])
            print(f"Added page {current_page + 1} as is.")
            current_page += 1
    
    # Write the output PDF
    with open(output_pdf_path, "wb") as out_file:
        writer.write(out_file)
    
    print(f"Reorganized PDF saved as '{output_pdf_path}'.")

if __name__ == "__main__":
    # Define input and output PDF paths
    input_pdf = "input.pdf"    # Replace with your input PDF path
    output_pdf = "output.pdf"  # Desired output PDF path
    
    # Define the list of ranges to merge
    # Example: Merge pages 2-4 and 7-10
    merge_ranges = ['2-4', '5-7']  # Replace or modify as needed
    
    # Check if input PDF exists
    if not os.path.isfile(input_pdf):
        print(f"Input PDF '{input_pdf}' not found.")
    else:
        reorganize_pdf(input_pdf, output_pdf, merge_ranges)
