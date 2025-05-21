"""
Создаёт индекс документов для последующего RAG.

Есть возможность индексировать, как pdf, так текстовые файлы
Исходно, использует относительный путь для этого файла
"""

from PyPDF2 import PdfReader
from langchain_community.vectorstores.faiss import FAISS
from models import NomicEmbedModel as embed
from models.config import NomicEmbedAPIConfig as model_config
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from typing import List
from pathlib import Path
from config import load_environment, validate_environment


def split_paragraphs(rawText):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    return text_splitter.split_text(rawText)


def load_pdfs(DOCUMENTS_PATH) -> List[str]:
    docs = os.listdir(DOCUMENTS_PATH)
    text_chunks = []  # Создаем пустой список для хранения текстовых фрагментов
    # Проходим по всем PDF-файлам
    for doc in docs:
        try:
            with open(f"{DOCUMENTS_PATH}/{doc}", "rb") as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    raw = page.extract_text()
                    chunks = split_paragraphs(raw)
                    text_chunks += chunks
        except Exception as e:
            print(f"SOME ERROR HAPPENED WHILE PROCESSING {doc} {e}")

    # Возвращаем список текстовых фрагментов
    return text_chunks


def load_text(DOCUMENTS_PATH) -> List[str]:
    docs = os.listdir(DOCUMENTS_PATH)
    text_chunks = []  # Создаем пустой список для хранения текстовых фрагментов
    for doc in docs:
        # try:
        with open(f"{DOCUMENTS_PATH}/{doc}", "r") as file:
            text = file.read()
            chunks = split_paragraphs(text)
            text_chunks += chunks
    # except Exception as e:
    #    print(f'SOME ERROR HAPPENED WHILE PROCESSING {DOCUMENTS_PATH}/{doc} {e}')

    return text_chunks


def process_documents():
    root_path = Path(__file__).resolve().parents[1] / "database"

    DOCUMENTS_PATH = "documents"
    DESTINATION_PATH = "faiss_db"

    print("LOADING FILES...")
    text_chunks = load_pdfs(root_path / DOCUMENTS_PATH)
    print("DONE!")

    print("EMBEDDING FILES...")
    store = FAISS.from_texts(text_chunks, embed(config=model_config()))
    print("DONE!")

    # Запись индекса на диск
    print(f"SAVING INDEX TO {root_path / DESTINATION_PATH}...")
    store.save_local(root_path / DESTINATION_PATH)
    print("DONE!")


load_environment()
validate_environment()
process_documents()
