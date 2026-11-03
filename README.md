# slbb-chatcut-huoke

通过 WorkBuddy、豆包工作、Codex 等宿主调用 ChatCut 客户端，完成一条口播或讲解视频的剪辑。适用于获客、知识分享、产品介绍和演示讲解等内容，不限定一分钟时长。

**当前版本：v2.7.1**

## 下载与安装

- [下载完整安装包](https://github.com/slbb1995/slbb-chatcut-huoke/releases/latest/download/slbb-chatcut-huoke-v2.7.1.zip)
- [版本与校验文件](https://github.com/slbb1995/slbb-chatcut-huoke/releases/latest)

1. 下载上面的完整安装包，在所用宿主支持的 Skill 导入入口导入；需要目录安装时，使用解压后的 `slbb-chatcut-huoke` 文件夹，保留其中全部文件。
2. 打开并登录 ChatCut 客户端，确认宿主能够调用它的剪辑工具。安装 Skill 本身不会自动安装 ChatCut 或完成连接配置。
3. 提供一条主口播视频；讲稿、产品或场景素材、背景音乐可按需附上。
4. 输入：`使用 slbb-chatcut-huoke，帮我剪这条口播。剪完先给我预览，确认后再导出正式成片。`

## 剪辑流程

先提取完整口播文案，清理明显口误、重复、卡壳和多余停顿，保留原意与自然气口；按素材安排字幕、主题标题、B-Roll、同步真人小窗、必要降噪和轻配乐。剪完提供预览，确认当前版本后正式导出。

默认成片为 9:16、1080×1920、30fps、H.264 MP4。具体剪辑和保存要求以当次指令及 Skill 正文为准。

- [完整 Skill](slbb-chatcut-huoke/SKILL.md)
- [使用说明](slbb-chatcut-huoke/使用说明.md)
- [一键提示词](slbb-chatcut-huoke/一键提示词.txt)
- [更新日志](slbb-chatcut-huoke/CHANGELOG.md)

本版统一技能名称与安装目录，保留发布前当前版本的剪辑能力。安装包包含参考文档、辅助脚本和内置音乐，不含个人安装元数据。此次发布已检查包结构与文件一致性，未重新执行各宿主的视频剪辑测试。
