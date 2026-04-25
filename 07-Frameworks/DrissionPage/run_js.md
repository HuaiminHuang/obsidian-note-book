---
title: 浏览器内 Fetch 模式 (run_js + Promise)
tags: [framework, drissionpage, fetch, javascript]
date: 2026-04-18
status: verified
difficulty: advanced
---

# 浏览器内 Fetch 模式参考

通过 DrissionPage 的 `tab.run_js()` 在浏览器内执行 `fetch()`，绕过 TLS 指纹检测。

## 核心原因

`run_js(code)` 会把代码包裹成 `function(){ ... }` 执行，不是 `async function`。
因此**不能用顶层 `await`**，必须用 `new Promise()` 包装异步操作。

```javascript
// ✗ 错误 —— run_js 不支持顶层 await
const resp = await fetch(url, options);
const data = await resp.json();
return data;

// ✓ 正确 —— 用 Promise 包装
return new Promise((resolve, reject) => {
    fetch(url, options)
        .then(r => r.json())
        .then(data => resolve(JSON.stringify(data)))
        .catch(err => reject(err.toString()));
});
```

## 完整模板代码

```python
import json

def _fetch(tab, url: str, payload: dict) -> dict | None:
    body = json.dumps(payload)
    js = f"""
    return new Promise((resolve, reject) => {{
        fetch('{url}', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json;charset=UTF-8'}},
            body: JSON.stringify({body})
        }})
        .then(r => r.json())
        .then(data => resolve(JSON.stringify(data)))
        .catch(err => reject(err.toString()));
    }});
    """
    try:
        raw = tab.run_js(js)
        if not raw:
            return None
        return json.loads(raw)
    except Exception as e:
        return None
```

## 数据流向

```
Python 层                              浏览器层                           服务器
─────────                              ────────                           ─────

dict payload
    │
    ├── json.dumps() ──→ JSON 字符串
    │                        │
    │                  f-string 嵌入 JS
    │                        │
    │                  tab.run_js(js)
    │                        │
    │                   ┌────▼────┐
    │                   │ fetch() │ ──POST──→ 接收请求
    │                   │ (浏览器) │          │
    │                   └────┬────┘     ←── 响应 JSON
    │                        │
    │                  r.json() 解析
    │                        │
    │                  JSON.stringify()
    │                        │
    │                  resolve(字符串)
    │                        │
    ├── raw = tab.run_js() ←─┘  (返回 Python str)
    │
    ├── json.loads(raw) ──→ dict
    │
    ▼
  返回结果
```

## 踩坑记录

### 1. f-string 花括号转义

JS 代码通过 Python f-string 构建，JS 中的 `{}` 需要写成 `{{}}`：

```python
# ✗ 错误 —— Python f-string 把 {url} 当变量
js = f"fetch('{url}', {method: 'POST'})"

# ✓ 正确 —— JS 的 {} 写成 {{}}
js = f"""
return new Promise((resolve, reject) => {{
    fetch('{url}', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({body})
    }})
}});
"""
```

### 2. 返回值必须是可序列化的

`run_js` 返回值通过 CDP 协议传输，支持：
- 字符串、数字、布尔值
- 简单 JS 对象（会自动转为 Python dict）
- **不支持**复杂对象（如 Response 对象）

所以 fetch 结果必须 `JSON.stringify()` 转成字符串，Python 端再 `json.loads()` 解析。

### 3. Cookie 自动携带

浏览器内 `fetch()` **自动携带当前页面的 cookie**，不需要手动设置 `headers['Cookie']`。

这是相比 `requests` 的一个优势——不需要从 tab 提取 cookie 再传入。

### 4. 超时处理

浏览器 `fetch` 默认无超时。如果需要超时控制：

```javascript
const controller = new AbortController();
setTimeout(() => controller.abort(), 10000);

fetch(url, { signal: controller.signal, ... })
    .then(r => r.json())
    .then(data => resolve(JSON.stringify(data)))
    .catch(err => reject(err.toString()));
```

### 5. headers 只需要 Content-Type

浏览器内 fetch 会自动附加：
- `Cookie`（当前域的 cookie）
- `Origin`（当前页面的 origin）
- `Referer`（当前页面 URL）

所以 JS 中只需要设置 `Content-Type`，不需要像 `requests` 那样手动构造完整 headers。

## 适用场景

| 场景 | 是否适合用这个模式 |
|------|-------------------|
| 服务端检测 TLS 指纹 | ✓ 核心场景 |
| 需要复用浏览器 cookie/session | ✓ 免去手动提取 |
| API 有 CORS 限制 | ✓ 同源请求无 CORS 问题 |
| 高频大量请求 | △ 偏慢（走 CDP → JS → fetch），考虑 Listener 拦截 |
| 不需要浏览器环境的普通 API | ✗ 直接用 `requests` 更简单 |

## 与 Listener 模式对比

| 维度 | run_js fetch | Listener 监听 |
|------|-------------|--------------|
| 主动/被动 | 主动发起请求 | 被动拦截页面发出的请求 |
| 适用场景 | 需要主动调 API | 页面操作触发请求，拦截拿数据 |
| 速度 | 中等（CDP + JS 执行开销） | 快（只拦截） |
| 控制力 | 完全控制请求参数 | 只能观察，不能修改请求 |

Listener 模式参考：`docs/examples/network-listen.md`