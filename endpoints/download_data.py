import json
import logging

from tqdm import tqdm

from backend.core.process_data.download_data import ArxivDownloader


logger = logging.getLogger(__name__)


def main(data_path: str, save_dir: str) -> None:

    downloader = ArxivDownloader(save_dir=save_dir)
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for row in tqdm(data):
        arxiv_id = row["id"]
        logger.info(f"Скачиваем PDF для arXiv ID: {arxiv_id}")
        try:
            file_path = downloader.download_pdf(arxiv_id)
            logging.info(f"PDF успешно сохранён в: {file_path}")
        except Exception as e:
            logging.error(f"Ошибка: {e}")


if __name__ == "__main__":
    save_dir = "data/interim"
    data_path = "data/processed/arxiv-filtered-data.json"
    main(data_path=data_path, save_dir=save_dir)
