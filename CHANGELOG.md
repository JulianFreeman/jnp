# 版本日志

## v0.3.7

- 修复 dict 中 `get_with_chained_keys` 函数的bug
- 优化 path 中的 `get_log_dir`
- gui.misc 添加 `create_mono_icon`，`create_round_icon_from_pixmap`
- `CheckUpdateButton` 提供了默认网址

## v0.3.6

- 修复未安装可选依赖时报错的问题

## v0.3.5

- gui.misc 增加 `FakeLogger`
- gui 增加 `CheckUpdateButton`

## v0.3.4

- 调整 `run_some_task` 的提示窗口堵塞

## v0.3.3

- misc 增加 `get_excepthook_for`
- gui 增加 `DebugOutputButton` 和 `run_some_task`
- `StyleComboBox` 提供修改默认值的参数

## v0.3.2

- 增加 `IconPushButton` 和 `get_icon_from_svg`
- 更新 `Card` 的关闭按钮
- 删除了 gui.misc 中几个不用的函数

## v0.3.1

- `Card` 支持设置图标
- `CardsArea` 在移除 `Card` 时会发出信号

## v0.3.0

- 升级 `PushButtonWithId` 为 `PushButtonWithItem` 以支持更多类型
- 增加 `CardsArea` 和 `Card` 类

## v0.2.0

- 合并了 pyside6 的工具集，作为可选内容

## v0.1.1

- 简化 `jnp.path.get_log_dir`
- 增加 pyproject.toml

## v0.1.0 (2024年8月12日 更新)

- 重整文件结构并更名为 `jnp`
- 移除 pyside6 相关内容到独立的库
- 增加部分函数

## 2024年7月10日 更新

- 重整文件结构
- 增加 `pyside6/styles_combobox`
- 修复 `functions::get_with_chained_keys` 的 bug
