---
title: TLS 指纹与浏览器内 Fetch
tags: [framework, drissionpage, tls, fingerprint, troubleshooting]
date: 2026-04-18
status: completed
difficulty: advanced
---

# TLS 指纹导致 Python requests 被静默拒绝

## 现象

微信小店客服 API (`store.weixin.qq.com`) 对 `requests` 发出的请求返回**正常响应但不包含数据**。

具体表现：`search_global` API 用 `requests.post()` 调用时：
- 当前活跃会话的用户（如 H2M）→ 能搜到
- 其他用户（如"厚德载物"、"大药房15692300538"）→ 返回 `user_hits_total_num=0`
- 同样的参数通过浏览器 `fetch()` → 所有用户都能搜到

服务端**不报错、不返回 403**，只是静默降级返回空数据。

## 排查过程

### 1. 检查 cookies

从 DrissionPage 提取全部 cookie，逐个对比 `requests` 请求中携带的值：

```
cookie 名称        requests 值    浏览器值     一致？
biz_magic          xxx           xxx         ✓
slave_sid          xxx           xxx         ✓
slave_user         xxx           xxx         ✓
... (共5个)                                    全部 ✓
```

结论：cookie 完全一致，不是问题。

### 2. 检查 headers

对比 `requests` 发送的 headers 和浏览器 Network 面板中看到的 headers：

```
Content-Type       ✓ 一致
Origin             ✓ 一致
Referer            ✓ 一致
User-Agent         ✓ 手动设置了同样的值
biz_magic          ✓ 一致
kf_scene           ✓ 一致
```

结论：headers 全部一致，不是问题。

### 3. 用 curl 测试

从浏览器 "Copy as cURL" 导出完整请求，在终端执行 → 能搜到所有用户。

把 cURL 中的 cookie 和 headers 搬到 Python `requests` → 搜不到。

结论：问题不在参数层面，在**请求来源的底层特征**。

### 4. 锁定根因：TLS 指纹

TLS 握手过程中，客户端会发送：
- 支持的加密套件列表（cipher suites）
- TLS 扩展列表及顺序
- 椭圆曲线参数

这些信息组合成 **JA3/JA4 指纹**，不同 HTTP 客户端的指纹完全不同：

| 客户端 | TLS 库 | JA3 指纹特征 |
|--------|--------|-------------|
| Chrome/Browser | BoringSSL | 特定的 cipher suite 顺序和扩展组合 |
| Python requests | OpenSSL (urllib3) | 不同的 cipher suite 顺序 |
| curl (系统) | OpenSSL/NSS | 又是不同的顺序 |

微信服务端通过 JA3 指纹识别请求来源：
- 指纹 = 真实浏览器 → 正常返回数据
- 指纹 = Python/curl（取决于编译方式）→ 静默降级

此外，**HTTP/2 帧特征**（SETTINGS 帧、WINDOW_UPDATE、HEADERS 帧的编码方式）也是辅助判断依据。Python `httpx` 的 h2 实现和 Chrome 的 HTTP/2 栈行为有细微差异。

## 结论

**凡是微信 store 后台 API，如果 `requests` 能用就用 `requests`（省事），如果发现数据异常就用浏览器内 `fetch`。**

不能用 `requests` 模拟浏览器的 TLS 指纹——即使强行伪造 JA3（如用 `curl_cffi`），也未必覆盖所有检测维度。浏览器已经连着了，直接让它发请求是最可靠的方案。

## 判断标准

| 场景 | `requests` 可行？ | 说明 |
|------|-------------------|------|
| `wx_shipping_insurance_adapter` 的保险查询 API | ✓ 可以 | 该 API 未做 TLS 指纹检测 |
| 微信客服 `search_global` | ✗ 不行 | TLS 指纹检测 + 静默降级 |
| 微信客服 `get_room_msg` | 未测试 | 既然搜索要走 fetch，消息也一起走 fetch |
| 微信客服 `get_session_summary` | 未测试 | 同上，统一走 fetch |

**实用原则**：先用 `requests` 试，如果数据异常（空结果、缺失字段）且参数确认无误，切换到浏览器 fetch。

## 参考链接

- JA3 指纹：https://engineering.salesforce.com/tls-fingerprinting-with-ja3-and-ja3s-247362855967/
- JA4 指纹（更新版）：https://blog.foxio.io/ja4%2B-network-fingerprinting
- `curl_cffi`（Python 伪造 TLS 指纹的库）：https://github.com/lexiforest/curl_cffi