# Demo 素材说明

## 推荐素材格式

- `assets/demo.gif`（GitHub README 可直接播放）
- 或 `assets/demo.mp4`（体积更小，建议配合 Release / 链接展示）

## 当前做法

项目内置了一个示例动效生成脚本：

```bash
python assets/generate_demo_gif.py
```

会生成：

- `assets/demo.gif`

## 替换为真实录屏

1. 使用 ScreenToGif / OBS 录屏（建议 8~12 秒）
2. 分辨率建议：`1280x720` 或 `960x540`
3. 控制体积：建议 `< 10MB`
4. 覆盖 `assets/demo.gif`
5. 提交并推送到 GitHub，README 会自动更新展示
