---
name: rag-pipeline
description: Build and optimize Retrieval-Augmented Generation pipelines with document chunking, embedding selection, vector DB setup, reranking, and evaluation. This skill should be used when building RAG systems, improving retrieval quality, or setting up vector search.
---

# RAG Pipeline Skill

## Overview

This skill guides building and optimizing RAG (Retrieval-Augmented Generation) pipelines, covering document chunking strategies, embedding model selection, vector database setup, retrieval fusion and reranking, and evaluation metrics.

## When to Use This Skill

- Building a new RAG pipeline from scratch
- Improving retrieval quality for an existing system
- Choosing between vector databases
- Optimizing document chunking
- Adding reranking or hybrid search
- Evaluating RAG pipeline performance

## RAG Architecture

```
Documents → Chunking → Embedding → Vector DB
                                        ↓
Query → Embedding → Retrieval → Reranking → LLM → Response
```

## Document Chunking Strategies

### Strategy Comparison

| Strategy | Best For | Chunk Size | Overlap |
|----------|----------|------------|---------|
| Fixed-size | Simple docs, homogeneous content | 512-1024 tokens | 50-100 tokens |
| Recursive | Mixed content, general purpose | 500-1000 tokens | 100-200 tokens |
| Semantic | Complex docs, varied topics | Variable | N/A |
| Document-based | Structured docs (HTML, MD) | By section | N/A |
| Sentence-window | High precision needs | 1 sentence + window | N/A |

### Implementation

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# General purpose - good default
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# For code
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=1000,
    chunk_overlap=100,
)

# Semantic chunking
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

semantic_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90,
)
```

### Chunking Best Practices

- Include metadata (source, page, section) with every chunk
- Preserve document hierarchy (titles, headers) in chunks
- Test multiple chunk sizes - measure retrieval quality, not just speed
- For tables, keep the full table as one chunk
- For code, chunk by function/class boundaries

## Embedding Model Selection

### Model Comparison

| Model | Dimensions | Speed | Quality | Cost |
|-------|-----------|-------|---------|------|
| `text-embedding-3-small` (OpenAI) | 1536 | Fast | Good | $0.02/1M tokens |
| `text-embedding-3-large` (OpenAI) | 3072 | Medium | Best | $0.13/1M tokens |
| `voyage-3` (Voyage AI) | 1024 | Fast | Excellent | $0.06/1M tokens |
| `BAAI/bge-large-en-v1.5` (local) | 1024 | Variable | Good | Free |
| `nomic-embed-text` (local) | 768 | Fast | Good | Free |

### Selection Guide

- **Production with budget**: `text-embedding-3-small` or `voyage-3`
- **Best quality**: `text-embedding-3-large` or `voyage-3`
- **Local/private data**: `BAAI/bge-large-en-v1.5` or `nomic-embed-text`
- **Multilingual**: `text-embedding-3-large` with language prefix

```python
# OpenAI embeddings
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Local embeddings with sentence-transformers
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
```

## Vector Database Setup

### Quick Comparison

| Database | Type | Best For | Scaling |
|----------|------|----------|---------|
| **LanceDB** | Embedded | Local dev, prototyping | Single node |
| **Qdrant** | Self-hosted / Cloud | Production, filtering | Horizontal |
| **Pinecone** | Managed cloud | Serverless, easy setup | Automatic |
| **Chroma** | Embedded | Prototyping | Single node |
| **pgvector** | PostgreSQL extension | Existing Postgres stack | Vertical |

### LanceDB (Local Development)

```python
import lancedb
from langchain_community.vectorstores import LanceDB

db = lancedb.connect("./lancedb")
vectorstore = LanceDB.from_documents(
    documents=chunks,
    embedding=embeddings,
    connection=db,
    table_name="my_docs",
)

# Query
results = vectorstore.similarity_search("query", k=5)
```

### Qdrant (Production)

```python
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
vectorstore = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="my_docs",
    client=client,
)

# With metadata filtering
from qdrant_client.models import Filter, FieldCondition, MatchValue
results = vectorstore.similarity_search(
    "query",
    k=5,
    filter=Filter(must=[
        FieldCondition(key="source", match=MatchValue(value="api_docs"))
    ]),
)
```

### Pinecone (Managed)

```python
from langchain_pinecone import PineconeVectorStore
import os

vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name="my-index",
)
```

## Retrieval Strategies

### Basic Retrieval

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},
)
```

### Hybrid Search (Dense + Sparse)

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Sparse retriever (keyword-based)
bm25_retriever = BM25Retriever.from_documents(chunks, k=5)

# Dense retriever (embedding-based)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Ensemble with weighted fusion
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.3, 0.7],
)
```

### Reranking

```python
# Cohere reranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

reranker = CohereRerank(model="rerank-v3.5", top_n=3)
reranking_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=hybrid_retriever,
)

# Cross-encoder reranker (local)
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
reranker = CrossEncoderReranker(model=model, top_n=3)
```

### Multi-Query Retrieval

```python
from langchain.retrievers import MultiQueryRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm,
)
```

## Full RAG Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context.
If the context doesn't contain the answer, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:""")

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": reranking_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("How does authentication work?")
```

## Evaluation Metrics

### Key Metrics

| Metric | Measures | Target |
|--------|----------|--------|
| **MRR** (Mean Reciprocal Rank) | Is the right doc ranked first? | > 0.7 |
| **NDCG@k** | Quality of top-k ranking | > 0.6 |
| **Recall@k** | Are all relevant docs in top-k? | > 0.8 |
| **Faithfulness** | Does answer match retrieved context? | > 0.9 |
| **Answer Relevancy** | Does answer address the question? | > 0.8 |

### Evaluation with RAGAS

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

eval_data = {
    "question": ["How does auth work?"],
    "answer": ["Auth uses JWT tokens..."],
    "contexts": [["JWT authentication is..."]],
    "ground_truth": ["The system uses JWT..."],
}

dataset = Dataset.from_dict(eval_data)
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)
print(results)
```

## Pipeline Optimization Checklist

- [ ] Test chunk sizes: 256, 512, 1024 tokens
- [ ] Compare at least 2 embedding models
- [ ] Add hybrid search (BM25 + dense)
- [ ] Add reranking step
- [ ] Set up evaluation dataset (50+ Q&A pairs)
- [ ] Measure latency at each stage
- [ ] Add metadata filtering where applicable
- [ ] Cache frequent queries
