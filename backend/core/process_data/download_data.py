import logging
import os

import requests


logger = logging.getLogger(__name__)


class ArxivDownloader:
    """A class for downloading PDF files from arXiv based on arXiv IDs."""

    def __init__(self, save_dir="./", pdf_url_template="https://arxiv.org/pdf/{}.pdf"):
        self.save_dir = save_dir
        self.pdf_url_template = pdf_url_template
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def download_pdf(self, arxiv_id):
        """
        Downloads a PDF file from arXiv using the provided arXiv ID.

        Args:
            arxiv_id (str): The arXiv identifier in the format 'YYMM.NNNNN' or similar.

        Returns:
            str: The file path of the saved PDF.

        Raises:
            Exception: If the HTTP request fails (status code is not 200).
        """
        pdf_url = self.pdf_url_template.format(arxiv_id)
        response = requests.get(pdf_url, timeout=(5, 15))
        if response.status_code != 200:
            raise Exception(f"Failed to download PDF: {response.status_code}")

        file_path = os.path.join(self.save_dir, f"{arxiv_id}.pdf")
        with open(file_path, "wb") as f:
            f.write(response.content)

        logger.info("PDF is saved to %s", file_path)

        return file_path
