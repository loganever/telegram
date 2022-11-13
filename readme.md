# 获得api_id和api_hash
https://core.telegram.org/api/obtaining_api_id
# 安装依赖包
pip3 install telethon

pip3 install xlwt
# 配置
配置config.ini,输入用户名，api、channel的链接或者id、最多找多少条聊天记录、聊天记录保存路径
# 运行代码
python3 main.py

首次登录需要输入手机号，验证码，之后不需要

telegram客户端可以直接导出聊天记录，但是每次查询都要导出很麻烦，调用api只需要第一次登录就行了，之后可以直接运行获取