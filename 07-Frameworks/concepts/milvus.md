---
title: Milvus - 开源向量数据库
tags: [python, framework, database, vector-db, milvus, ai]
date: 2026-03-15
status: learning
difficulty: advanced
---

# Milvus - 开源向量数据库

## 概念

Milvus 是一个开源的、云原生向量数据库，专为 AI 应用设计，支持高维向量数据的存储、检索和相似性搜索。

**主要特点**：
- 云原生：支持大规模向量数据
- 高性能：支持十亿级向量检索
- 灵活：支持多种距离度量
- 兼容性：兼容 OpenAI 和其他向量搜索 API

## 安装

```bash
# Docker 安装
docker run -d --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:latest

# 启动 Milvus
docker start milvus-standalone
```

## 基本使用

### 1. 安装 Python 客户端

```bash
pip install pymilvus
```

### 2. 连接 Milvus

```python
from pymilvus import connections, utility

# 连接
connections.connect("default", host="localhost", port="19530")

# 检查状态
print(utility.list_collections())
```

### 3. 创建集合

```python
from pymilvus import Collection, FieldSchema, CollectionSchema, DataType

# 定义字段
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128),
    FieldSchema(name="label", dtype=DataType.VARCHAR, max_length=50)
]

# 创建 schema
schema = CollectionSchema(fields, description="Example collection")

# 创建集合
collection = Collection(name="example_collection", schema=schema)
print(f"Collection {collection.name} created")
```

### 4. 插入数据

```python
import numpy as np

# 生成向量数据
embeddings = np.random.randn(1000, 128).astype('float32')
ids = list(range(1000))
labels = [f"label_{i}" for i in range(1000)]

# 插入数据
data = [ids, embeddings, labels]
collection.insert(data)

# 刷新
collection.flush()
```

### 5. 创建索引

```python
# 创建 IVF_FLAT 索引
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128}
}

collection.create_index("embedding", index_params)
```

### 6. 向量搜索

```python
# 准备查询向量
query_vectors = np.random.randn(10, 128).astype('float32')

# 搜索参数
search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 16}
}

# 执行搜索
results = collection.search(
    data=query_vectors,
    anns_field="embedding",
    param=search_params,
    limit=5,
    expr=None,
    output_fields=["label"]
)

# 处理结果
for i, res in enumerate(results):
    print(f"Query {i}:")
    for j, hit in enumerate(res):
        print(f"  Result {j}: id={hit.id}, score={hit.distance}, label={hit.entity.get('label')}")
```

## 实际应用

### 1. 文本相似性搜索

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from sentence_transformers import SentenceTransformer

# 连接 Milvus
connections.connect("default", host="localhost", port="19530")

# 创建集合
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
]
schema = CollectionSchema(fields, description="Text search collection")
collection = Collection(name="text_search", schema=schema)

# 生成嵌入
model = SentenceTransformer('all-MiniLM-L6-v2')

# 插入文档
texts = [
    "Python is a popular programming language.",
    "Machine learning uses algorithms.",
    "Flask is a lightweight framework.",
    "SQLAlchemy is an ORM tool."
]

embeddings = model.encode(texts)
collection.insert([texts, embeddings])
collection.flush()

# 创建索引
collection.create_index("embedding", {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 16}})

# 搜索相似文本
query = "What is a popular programming language?"
query_embedding = model.encode([query])

results = collection.search(
    data=query_embedding,
    anns_field="embedding",
    param={"metric_type": "L2", "params": {"nprobe": 16}},
    limit=2
)

print(f"Query: {query}")
for res in results:
    for hit in res:
        print(f"  {hit.entity.get('text')} (score: {hit.distance:.2f})")
```

### 2. 图像相似性搜索

```python
from PIL import Image
import requests

# 加载图像
url = "https://example.com/image.jpg"
image = Image.open(requests.get(url, stream=True).raw)

# 生成嵌入（使用预训练模型）
from transformers import CLIPProcessor, CLIPModel
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

inputs = processor(images=image, return_tensors="pt")
image_embedding = model.get_image_features(**inputs).detach().numpy()[0]

# 搜索相似图像
results = collection.search(
    data=[image_embedding],
    anns_field="embedding",
    param={"metric_type": "L2", "params": {"nprobe": 16}},
    limit=5
)
```

## 相关资源

- [Milvus 官方文档](https://milvus.io/)
- [pymilvus 文档](https://milvus.io/api-reference/pymilvus/v2.3.x/About.md)

## 相关笔记

- [[redis]] - Redis 数据库
- [[mysql]] - MySQL 数据库

---

**创建日期**: 2026-03-15
**最后更新**: 2026-03-15
