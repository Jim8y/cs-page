---
layout: post
tags: [Python, Development]
title: Generating requirements.txt automatically
---

[`pipreqs`](https://github.com/bndr/pipreqs) is a useful tool to generate
pip requirements.txt file based on `import`s of any Python project.

```shell
pip install pipreqs
pipreqs /path/to/project/
```
