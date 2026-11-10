# X 上值得关注的人

按主题整理的 X（Twitter）阅读清单：创业与产品、思维与投资、AI 与 Agent、人文、教育与儿童成长，外加一份 Thariq 专题。每个人一段简介，配上 2026 年最值得读的帖子。

线上地址：https://x-reading-list.pages.dev

数据截至 2026-11-10；简介中标 * 的内容来自常识，未从帖子中核实。

## 结构

- `src-*.txt`：每份清单的原始内容
- `data.json`：站点数据的唯一来源，更新内容直接改这里
- `src-*.txt` / `parse.py`：最初从清单页面导出的原始内容和解析脚本，已落后于 `data.json`，不要再运行 `parse.py`，否则会覆盖更新
- `build.py` + `style.css` + `site.js`：生成静态页面到 `dist/`
- `mkworker.py`：把 `dist/` 打包成 Cloudflare Pages 的 `_worker.js`，并生成部署脚本 `deploy2.js`
- `serve.py`：本地预览；`shots.py`：截图

## 构建与发布

```bash
python3 build.py && python3 mkworker.py
python3 serve.py   # 本地预览
```

然后用 Cloudflare 的 API 执行 `deploy2.js`，部署到 Pages 项目 `x-reading-list`。
