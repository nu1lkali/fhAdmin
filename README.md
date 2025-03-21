# 烽火光猫超密获取工具

这是一个Python脚本，旨在通过Telnet从烽火光猫设备中获取管理员用户名和密码。该脚本首先尝试通过HTTP请求激活目标设备上的Telnet服务，然后使用Telnet连接到设备并发送命令以检索管理凭据。仅自有设备测试有效。

## 工作原理

1. **输入验证**：脚本首先检查用户提供的IP地址和MAC地址格式是否正确。
2. **激活Telnet服务**：通过向设备的特定URL（例如`http://<ip>/cgi-bin/telnetenable.cgi?telnetenable=1&key=<mac>`）发送HTTP GET请求来激活Telnet服务。
3. **建立Telnet连接**：一旦Telnet服务被激活，脚本将创建一个TCP连接到设备的Telnet端口（默认为23），并通过该连接发送命令。
4. **发送命令并接收响应**：脚本通过Telnet连接发送一系列命令，包括登录凭据和查询管理用户名及密码的命令，并解析返回的数据以提取所需信息。
5. **输出结果**：最终，提取的管理员用户名和密码将以清晰直观的方式显示给用户。

## 功能特点

- 验证输入的IP地址和MAC地址格式是否正确。
- 通过HTTP请求激活Telnet服务。
- 使用Telnet协议与设备通信，获取管理员用户名和密码。
- 输出信息清晰直观，便于理解。

## 运行环境

- Python 3.7 或更高版本
- `requests` 库（可以通过 `pip install requests` 安装）

## 输出示例
- 当前IP地址为：192.168.1.1
- 当前MAC地址为：38:7A:3C:9C:CD:E0
- 向 http://192.168.1.1/cgi-bin/telnetenable.cgi?telnetenable=1&key=387A3C9CCDE0 发送请求以开启Telnet服务
- 管理员用户名: CMCCAdmin
- 管理员密码: CMCCAdmin*n5Ks7Cb


## 安装步骤

### 安装依赖

确保已安装了所需的Python库，可以使用以下命令进行安装：

```bash
pip install requests

