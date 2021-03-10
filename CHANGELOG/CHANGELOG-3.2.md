## 3.2.4 (Oct 27, 2020)
    * [optimization] 支持上传和下载时指定后缀
    * [bug fix] 修复默认参数为可变值, 导致行为和预期不一致的问题
    * [bug fix] 修复其他已知问题
## 3.2.5 (Jan 21, 2021)
    * [optimization] readme
    * [optimization] example
## 3.2.6 (Mar 10, 2021)
    * [optimization] readme
    * [optimization] 分片上传支持异步并发多线程
    * [optimization] file_etag函数size参数设置默认值
    * [bug fix] 开启线程时使用分片上传会阻塞
    * [bug fix] copy函数的srckey支持中文
    * [bug fix] 修复上传.tar.gz文件的MIME-Type错误，增加util.py中_EXTRA_TYPES_MAP的内容
    * [Deprecation] 废弃函数resumeuploadfile()
