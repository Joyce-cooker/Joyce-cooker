# 传到 GitHub（网页拖拽版）

这个文件夹就是完整的仓库内容，21 个文件，拖一次就完事。下面是**不出错**的做法。

---

## 一、先建空仓库

1. 打开 https://github.com/new
2. **Repository name**：`douyin-cover-playbook`
3. **Description**（可复制）：

   ```
   抖音封面方法论：诊断 → 规则 → 系统 → 案例。含 3:4 / 9:16 / 4:3 成品图与可复现的 Pillow 脚本
   ```

4. 可见性选 **Public**（或 Private，随意）
5. ⚠️ **不要勾** "Add a README file"、不要选 .gitignore、不要选 license——仓库必须是全空的
6. 点 **Create repository**

---

## 二、拖文件（关键一步）

建好后页面中间有个 **"uploading an existing file"** 链接，点进去。

然后：

1. 打开资源管理器，进到 `douyin-cover-playbook` 文件夹**里面**
2. **Ctrl + A 全选**（选中的是：`.gitignore`、`PUSH.md`、`README.md`、`assets`、`docs`、`images`、`scripts`）
3. 把这 7 项一起拖到网页上传框
4. 等进度条走完（约 5MB），下面 commit message 随便写，比如 `docs: 抖音封面方法论 + 熄灯之后案例`
5. 点 **Commit changes**

> ### ⚠️ 最容易踩的坑
> **不要拖文件夹本身**（`douyin-cover-playbook` 这个图标）。
> 拖了它，仓库里会变成 `douyin-cover-playbook/README.md` 这样多一层，
> 首页的 README 就不会自动展示了，而且网页上很难改回来，只能删库重建。
>
> 正确做法是**进到文件夹里面，全选内容再拖**。

> `PUSH.md`（本文件）你也一起传上去，回头自己看也方便。想精简的话不传也行。

---

## 三、上传后自检 30 秒

打开仓库首页，确认这四件事：

- [ ] 根目录直接看到 `README.md`（**不是** `douyin-cover-playbook/README.md`）
- [ ] 首页第一张图（诊断与改版前后对比）能正常显示
- [ ] `images/` 里是 8 个文件，`docs/` 里 3 个，`scripts/` 里 5 个
- [ ] 页面往下拉，目录表格里的三个文档链接点得开

顺手的加两件事：

- 仓库右上 **About** → 点齿轮 → **Topics** 填：
  `douyin` `cover-design` `poster-design` `pillow` `python` `content-creation`
- 勾上 About 里的 **Releases / Packages** 都无所谓，不用管

---

## 四、目录长什么样

```
douyin-cover-playbook/
├── README.md                     主文档：诊断 → 规则 → 系统 → 案例 → 清单
├── PUSH.md                       本文件
├── .gitignore
├── docs/
│   ├── diagnosis.md              诊断：6 个病灶 + 现场证据
│   ├── system.md                 版式系统：三元素 / 三级字号 / 70-20-10 / 6 模板
│   └── case-dorm.md              案例：《熄灯之后》完整参数与三次重排
├── images/                       8 张成品图与对比图
├── assets/
│   ├── source-frame.jpg          案例视频单帧（脚本输入）
│   └── before-github-cover.png   点评用截图（版权归原作者）
└── scripts/                      5 个 Pillow 脚本
```

---

## 五、以后想更新内容怎么办

网页上传没有 git 历史，每次修改都是「删文件→重传」或者单个文件编辑。

如果之后更新变多了，装个 Git 会舒服很多：

```bash
git clone https://github.com/<你的用户名>/douyin-cover-playbook.git
# 改完
git add . && git commit -m "update" && git push
```

或者直接用 GitHub 网页的铅笔图标改 markdown，改图才需要重传。

---

## 附：先在本地确认脚本能跑（可选）

```bash
pip install pillow numpy
python scripts/dorm_cover.py          # 3:4 / 9:16 三个文案版本
python scripts/dorm_cover_43.py       # 4:3 横版
python scripts/template_system.py     # 六种做法 + 前后对比
python scripts/case_comparison.py     # 原帧 vs 成品
```

输出落在 `out/`，已经在 `.gitignore` 里排除。

字体默认 `C:\Windows\Fonts\NotoSansSC-VF.ttf`，其他系统设环境变量 `COVER_FONT` 指到你的思源/Noto Sans SC 可变字体。
