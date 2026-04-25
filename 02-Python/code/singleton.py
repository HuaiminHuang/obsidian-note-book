"""
Singleton
单例模式的核心价值：
1. 控制实例数量 → 节省资源
2. 保证状态一致 → 全局唯一数据源
3. 提供全局访问 → 方便跨模块使用
"""


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init_once()
        return cls._instance

    def __init_once(self):
        self.settings = {"debug": False}

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key):
        return self.settings.get(key)


# 模块A
config_a = Config()
print(f"初始状态: {config_a.get('debug')}")
config_a.set("debug", True)
print("=" * 20)

# 模块B
config_b = Config()
print(f"True - 看到了模块A的修改: {config_b.get('debug')}")
# 体现作用：全局共享同一个配置状态 True
print(f"全局共享一个配置状态: {config_a is config_b}")
