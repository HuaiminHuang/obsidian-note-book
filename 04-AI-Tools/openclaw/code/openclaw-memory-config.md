---
title: OpenClaw 记忆系统完整配置参考
date: 2026-04-26
tags: [ai/openclaw, memory, config, embedding]
status: completed
---

# OpenClaw 记忆系统完整配置参考

配置文件位置：`~/.openclaw/openclaw.json`

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "fallback": "local",
        "model": "qwen3-embedding:0.6B",
        "chunking": {
          "tokens": 1024,
          "overlap": 128
        },
        "sync": {
          "onSessionStart": true,
          "onSearch": true,
          "watch": true
        },
        "cache": {
          "enabled": true,
          "maxEntries": 10000
        }
      }
    }
  },
  "plugins": {
    "entries": {
      "memory-core": {
        "enabled": true,
        "config": {
          "dreaming": {
            "enabled": true,
            "frequency": "daily",
            "timezone": "Asia/Shanghai",
            "storage": {
              "mode": "both"
            },
            "phases": {
              "light": {
                "enabled": true,
                "lookbackDays": 3,
                "limit": 50
              },
              "deep": {
                "enabled": true,
                "limit": 20,
                "minScore": 0.6,
                "minRecallCount": 2
              },
              "rem": {
                "enabled": true,
                "lookbackDays": 7,
                "limit": 10
              }
            }
          }
        }
      },
      "memory-wiki": {
        "enabled": true,
        "config": {
          "vaultMode": "bridge",
          "vault": {
            "path": "~/.openclaw/wiki/main",
            "renderMode": "native"
          },
          "bridge": {
            "enabled": true,
            "readMemoryArtifacts": true,
            "indexDreamReports": true,
            "indexDailyNotes": true,
            "indexMemoryRoot": true,
            "followMemoryEvents": true
          },
          "ingest": {
            "autoCompile": true,
            "maxConcurrentJobs": 1,
            "allowUrlIngest": true
          },
          "search": {
            "backend": "shared",
            "corpus": "all"
          },
          "context": {
            "includeCompiledDigestPrompt": false
          },
          "render": {
            "preserveHumanBlocks": true,
            "createBacklinks": true,
            "createDashboards": true
          }
        }
      }
    }
  }
}
```
