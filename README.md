# tape-viewer
A simple and fast tool for tape reading.

## 使用方法
**需要Python3!!!**

先安装`colored`、`tushare`和`pygame`包

config.json中配置自选股代码和是否报警

|字段|描述|
|---|---|
|index|指数（默认报警）|
|selection|自选股（可配置报警）|
|extra|他选股（默认不报警）|
|interval|刷新时间|
|warn|是否报警|

运行`$ python3 tape_viewer.py`

![](http://p2q6d37qm.bkt.clouddn.com/18-7-6/18491045.jpg)
