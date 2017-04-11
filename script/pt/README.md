# 葡萄PT监控
---
##  使用说明
- python 版本>=3.4
- 修改`Secrets.py`中:
	- siteUserName: 葡萄用户名
	- sitePassword: 葡萄密码
	- emailFromAddr: 邮件发送方
	- emailToAddr: 邮件接收方
	- emailPassword: 邮件发送方密码
- 执行命令
`python main.py & >/dev/null 2>&1`

## 功能
2017.04.11

- 爬取网站首页的种子列表，过滤出有价值的种子，邮件通知（发送到139邮箱会短信通知）
- 当魔力值小于一定阈值时，邮件通知
