import re
from datetime import datetime
from typing import List, Dict, Any

import pdfplumber

def extract_loss_run_data(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts loss run data from a PDF file.
    """
    extracted_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                data = parse_custom_loss_run_text(text)
                if data:
                    extracted_data.extend(data)
    return extracted_data


def parse_custom_loss_run_text(text: str) -> List[Dict[str, Any]]:
    """
    Parses the text extracted from the PDF according to the specific format of the uploaded loss run report.
    """
    results = []

    # Extract policy period
    policy_match = re.search(
        r'Policy Terms:\s*(\d{1,2}/\d{1,2}/\d{4})\s*-\s*(\d{1,2}/\d{1,2}/\d{4})',
        text
    )
    if not policy_match:
        print("Failed to match policy period")
        return results

    try:
        policy_start = datetime.strptime(policy_match.group(1), '%m/%d/%Y').date()
        policy_end = datetime.strptime(policy_match.group(2), '%m/%d/%Y').date()
    except ValueError as e:
        print(f"Failed to parse dates: {e}")
        return results

    # Extract policy number
    policy_number_match = re.search(r'Policy Numbers:\s*(\w+)', text)
    if not policy_number_match:
        print("Failed to match policy number")
        return results

    policy_number = policy_number_match.group(1)

    # Extract claims
    claim_pattern = r'(\d{1,2}/\d{1,2}/\d{4})\s+([A-Z])\s+([A-Z][A-Z\s]+(?:DAMAGED|DAMAGE)[^\$]+)\$?([\d,.]+)'
    for line in text.split('\n'):
        claim_match = re.search(claim_pattern, line.strip())
        if claim_match:
            try:
                claim_record = {
                    'policy_number': policy_number,
                    'policy_period_start': policy_start,
                    'policy_period_end': policy_end,
                    'loss_date': datetime.strptime(claim_match.group(1), '%m/%d/%Y').date(),
                    'status': 'Closed' if claim_match.group(2) == 'C' else 'Open',
                    'description': claim_match.group(3).strip(),
                    'total_incurred': float(claim_match.group(4).replace(',', ''))
                }
                results.append(claim_record)
                print(f"Successfully parsed claim: {claim_record}")
            except (ValueError, IndexError) as e:
                print(f"Error processing claim line '{line}': {e}")
                continue
        else:
            print(f"No claim match for line: {line}")

    return results
