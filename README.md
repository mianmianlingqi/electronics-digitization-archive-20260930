# 电子信息全量数字化归档

此仓库保存《完成电子信息全量数字化》聊天对应的原始资料、已完成成果、未完成稿、历史修订版本、图源、制作数据、验收证据和暂停断点。

资料数字化工作保持用户暂停状态。最后可靠台账为第十轮：**85份源文件、4263源页；12份整源验收完成，73份未整份完成；519源页覆盖，其中473页通过、46页待核；97对当前有效Word/PDF，共1357输出PDF页。**

## 查看与下载

- [当前有效的97对Word/PDF目录](current_outputs/目录.md)：每册均可直接下载，忠实稿与新增答案解析分开保存。
- [完整资料下载页](https://github.com/mianmianlingqi/electronics-digitization-archive-20260930/releases/tag/snapshot-20260930)：原始输入ZIP，以及保留原路径的项目快照分包。
- [全部85份源资料与状态](records/source_inventory.json)、[未完成处理队列](records/full_processing_queue.json)、[权威断点](records/checkpoint.json)、[用户暂停记录](records/user_pause.json)。
- [源页验收总账](records/source_page_coverage.json)与[第十轮最终接续记录](records/第十轮最终接续补记.md)。

完整快照包含**70,958个项目文件，原始大小11,533,821,106字节**，另有原始输入ZIP 1,512,607,026字节。历次成果、旧分册、草稿、渲染图、图源、脚本、工作记录都在快照中；不会把未验收稿记作完成。

## 快照的保存方式

GitHub普通仓库文件上限为100 MiB，因此完整资料使用同一私有仓库的Releases分包保存；当前有效成果与台账同时保存在仓库文件中。[GitHub大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)、[Release附件说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。

16个项目ZIP分包加1个原始输入ZIP，共17个附件。每个项目ZIP分包都可独立解压。全部解压到同一个目录，即可组合为`ExamBench/`项目快照，目录名和文件内容保留。`original-electronics-input.zip`是原始输入压缩包，原始目录及85个成员完整保留。

源文件未修改。JSON/Markdown中的原始`D:/02_Projects/active/ExamBench`路径仍作为历史来源记录；下载后的目录可通过文件清单对应。

本归档范围为电子信息项目。项目中另行存放的数学任务、游戏演示，以及`.git`、虚拟环境、`node_modules`等可重新安装的环境文件不计入此次资料快照；详见[范围说明](manifests/scope.json)。

## 完整性与恢复

每个文件记录原路径、大小、SHA256和所属附件；每个ZIP也保存SHA256。85份源文件和194份当前Word/PDF均与权威台账中的哈希核对。

完整下载入口见[17个附件下载目录](manifests/下载目录.md)；[附件SHA256](manifests/SHA256SUMS.txt)、[全部文件CSV清单](manifests/files.csv)、[全部文件JSON清单](manifests/files.json)与[85份源文件状态目录](records/源文件状态目录.md)均已保存。登录GitHub后，可从Releases页面下载所有附件，或使用已登录的GitHub CLI：

```text
gh release download snapshot-20260930 --repo mianmianlingqi/electronics-digitization-archive-20260930 --dir downloaded_assets
```

需要恢复超长Windows文件路径时，可用本仓库的恢复工具：

```text
python tools/restore_snapshot.py --assets downloaded_assets --destination restored
```

仅核验下载包，可用：

```text
python tools/restore_snapshot.py --assets downloaded_assets --verify-only
```

恢复工具会核对ZIP和每个文件的SHA256，已有不同内容的文件会停止覆盖。它只恢复文件，不运行原项目中的制作或台账初始化脚本。

## 归档核验结果

全部70,958个快照文件已从ZIP读回并逐个通过SHA256；17个Release附件均经GitHub返回的大小和SHA256核对；194份当前Word/PDF已与GitHub文件树及权威验收哈希核对。原始输入ZIP的85个成员与提取源文件逐个按哈希集合核对一致。详见[上传与完整性核验记录](records/archive_upload_verification.json)。
