import requests
import os
import logging

logger = logging.getLogger(__name__)

class ArxivDownloader:
    def __init__(self, save_dir='./', pdf_url_template='https://arxiv.org/pdf/{}.pdf'):
        self.save_dir = save_dir
        self.pdf_url_template = pdf_url_template
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def download_pdf(self, arxiv_id):
        pdf_url = self.pdf_url_template.format(arxiv_id)
        response = requests.get(pdf_url)
        if response.status_code != 200:
            raise Exception(f"Не удалось скачать PDF: код {response.status_code}")

        file_path = os.path.join(self.save_dir, f"{arxiv_id}.pdf")
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"PDF сохранён: {file_path}")
        return file_path