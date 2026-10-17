from pathlib import Path
from typing import Iterable
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from docx import Document as DocxDocument

SUPPORTED = {".pdf",".txt",".md","docx"}


def load_file(path: Path) -> list[Document]:
    suffix = path.suffix.lower()
    if(suffix==".pdf"):
        return PyPDFLoader(str(path)).load()
    elif(suffix==".txt" or suffix==".md"):
        return TextLoader(str(path), encoding="utf-8").load()
    elif(suffix==".docx"):
        doc=DocxDocument(str(path))
        doc_content= "\n".join(p.text for p in doc.paragrpahs if p.text.strip())
        return [Document(page_content=doc_content, metadata={"source": str(path)})]
    else:
        ValueError(f"Unsupported file type: {suffix}")

def chunk_documents(docs:Iterable[Document])-> list[Document]:
    text_splitter= RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120, add_start_index=True)
    return text_splitter.split_documents(list[Document](docs))