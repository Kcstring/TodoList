# Tomorrow Todo (Desktop)

一个本地运行、跨平台的桌面 Todo 应用，主打简洁暗色 UI + 启动粒子动画。

## 演示效果

> GitHub 首页会直接显示这个 GIF

![Demo](assets/demo.gif)

## 功能概览

- `今日 / 明日` 大按钮切换（默认显示今日）
- 任务新增、勾选完成、删除已完成、全部重置
- 本地 JSON 持久化（无服务器依赖）
- 启动动画（点展开 -> 旋转 -> 放大过渡）
- 窗口自动居中（Windows 工作区）
- 黑色粒子风应用图标（`assets/todo.ico`）

## 目录结构

```text
Todolist/
├─ main.py
├─ requirements.txt
├─ start_windows.bat
├─ start_windows_silent.vbs
├─ build_windows.ps1
├─ create_desktop_shortcut.ps1
├─ app/
│  ├─ __init__.py
│  ├─ storage.py
│  ├─ window_utils.py
│  ├─ splash.py
│  └─ ui.py
├─ assets/
│  ├─ todo.ico
│  └─ generate_icon.py
└─ data/
   └─ tasks.json
```

## 环境要求

- Python 3.9+
- Windows 推荐（已针对 Windows 启动与图标优化）

安装依赖：

```bash
pip install -r requirements.txt
```

## 运行方式

### 1) 开发运行

```bash
python main.py
```

### 2) Windows 脚本运行（无终端）

双击：

- `start_windows_silent.vbs`

或运行：

- `start_windows.bat`

## 今日 / 明日逻辑说明

- 每个任务包含字段：
  - `text`: 任务内容
  - `done`: 是否完成
  - `plan_date`: 计划日期（`YYYY-MM-DD`）
- 应用默认显示 `今日`
- 切换到 `明日` 后，只显示计划日期为明天的任务
- 新增任务会写入当前标签（今日或明日）

## 数据文件

数据保存在：

- `data/tasks.json`

示例：

```json
{
  "tasks": [
    {
      "text": "晨跑",
      "done": false,
      "plan_date": "2026-03-19"
    }
  ]
}
```

## 图标与打包

### 生成黑色粒子图标

```bash
python assets/generate_icon.py
```

输出：

- `assets/todo.ico`

### 生成演示 GIF（可上传到 GitHub 展示）

```bash
python assets/generate_demo_gif.py
```

输出：

- `assets/demo.gif`

### 打包为 exe

```powershell
.\build_windows.ps1
```

输出：

- `dist/TomorrowTodo.exe`

### 创建桌面快捷方式

```powershell
.\create_desktop_shortcut.ps1
```

输出：

- `Desktop/Tomorrow Todo.lnk`

快捷方式图标优先使用 `assets/todo.ico`。

## 常见问题

- 图标未刷新：按 `F5` 刷新桌面，必要时重启资源管理器
- 启动失败：查看项目根目录 `run.log`
- 任务丢失：检查 `data/tasks.json` 是否被外部清理
- 演示图不更新：替换 `assets/demo.gif` 后，重新 push 到 GitHub

