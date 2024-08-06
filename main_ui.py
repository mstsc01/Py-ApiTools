from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow,QApplication,QDialog,QCheckBox,QPushButton,QComboBox,QPlainTextEdit,QLineEdit,QStatusBar,QLabel,QMessageBox
import sys
from PyQt6.QtCore import QTimer,QThread, pyqtSignal

from datetime import datetime
from opt import all
from saconfig import read_config ,save_config

import pyperclip,requests

from designer2 import Ui_Form
from designer import Ui_MainWindow

def fetch_response_info(response):
    response_info = {
        'status_code': response.status_code,
        'text': response.text,
        'content': response.content,
        'headers': (response.headers),
        'url': response.url,
        'history': [r.status_code for r in response.history],
        'encoding': response.encoding,
        'cookies': response.cookies.get_dict() if response.cookies else {},
    }
    # print(response.status_code,response.content)
    # 尝试解析 JSON 响应，如果失败则返回 None
    try:
        response_info['json'] = response.json()
    except ValueError:
        response_info['json'] = None
    
    return response_info


    
def clear_text_edits(widget):
# 如果控件是 QPlainTextEdit，清空它的内容
    if isinstance(widget, QPlainTextEdit):
        widget.clear()
    # 递归地检查控件的子控件
    for child in widget.children():
        clear_text_edits(child)
def show_error_message(self,data):
    # 显示错误弹窗提示
    QMessageBox.critical(self, "错误", data)
# 定义一个线程类
class RequestThread(QThread):
    # 定义一个信号，用于传递请求结果回主线程
    result_signal = pyqtSignal(dict)

    def __init__(self,url,method,data=None,headers=None,cookies=None,proxies=None):
        super().__init__()
        self.url=url
        self.method=method
        self.data=data
        self.headers=headers
        self.cookies=cookies
        self.proxies=proxies

    def run(self):
        # 在线程中执行 HTTP 请求
        try:
            if self.method =="POST":
                print("post")
                response = requests.post(self.url,data=self.data,headers=self.headers ,proxies=self.proxies,verify=False,allow_redirects=False)  
                # print("ff",fetch_response_info(response)) 
            elif self.method == "GET":
                print("get")
                response = requests.get(self.url,headers=self.headers ,cookies=self.cookies,proxies=self.proxies,verify=False,allow_redirects=False)   
                # print("ff",fetch_response_info(response))
            response.raise_for_status()  # 将抛出异常，如果请求返回了失败的状态码
        except requests.RequestException as e:
            response = {"err":str(e)}
            self.result_signal.emit(response)
            return
        # 发送信号，传递请求结果回主线程
        data=fetch_response_info(response)
        self.result_signal.emit(data)
      
        
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # uic.loadUi("untitled.ui",self)
        
        self.ui = Ui_MainWindow()  # 创建 UI 类的实例
        self.ui.setupUi(self)
        

        self.__box()#注册控件
        self.__demo()#绑定行为
        self.__app()#启动功能/事件
    def __box(self):    
        self._请求方式: QComboBox=self.ui.comboBox
        self._数据格式: QComboBox=self.ui.comboBox_2
        #按钮注册 
        self._生成代码: QPushButton=self.ui.pushButton
        self._全部清空: QPushButton=self.ui.pushButton_2
        self._粘贴协议包: QPushButton=self.ui.pushButton_3
        self._发送请求: QPushButton=self.ui.pushButton_4
        #输入框注册
        self._请求地址: QPlainTextEdit=self.ui.plainTextEdit
        self._提交的数据: QPlainTextEdit=self.ui.plainTextEdit_2
        self._提交的ck: QPlainTextEdit=self.ui.plainTextEdit_3
        self._提交的协议头: QPlainTextEdit=self.ui.plainTextEdit_4
        self._响应正文: QPlainTextEdit=self.ui.plainTextEdit_5
        self._返回的协议头: QPlainTextEdit=self.ui.plainTextEdit_6
        self._返回的cookies: QPlainTextEdit=self.ui.plainTextEdit_7
        
        self._代理地址: QLineEdit=self.ui.lineEdit

        self._状态栏:QStatusBar=self.ui.statusbar
        self._使用系统代理: QCheckBox=self.ui.checkBox
        self._禁止重定向: QCheckBox=self.ui.checkBox_2

    def __demo(self):
        
        self._全部清空.clicked.connect(self.a)
        self._粘贴协议包.clicked.connect(self.b)
        self._发送请求.clicked.connect(self.c)
        self._使用系统代理.clicked.connect(self.d)

    def __app(self):
        self.ui.time_label = QLabel()
        self._状态栏.addPermanentWidget(self.ui.time_label)#添加标签控件

        # 更新时间标签的初始时间
        self.update_time()

        # 创建一个 QTimer，定时更新时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)  # 连接信号和槽
        self.timer.start(1000)  # 每1000毫秒（1秒）触发一次

    def update_time(self):
        # 获取当前时间并格式化为字符串
        current_time = datetime.now().strftime('%H:%M:%S')
        # 更新时间标签的文本
        self.ui.time_label.setText(f' | 当前时间: {current_time}')
    '''
    点击事件

    '''
    def a(self):
        print("_全部清空")
        clear_text_edits(self)
        

    def b(self):
        print("_粘贴协议包 \n")
        
       
        # 获取剪切板内容
        try:
            clipboard_content = pyperclip.paste()
        # print(clipboard_content)
        except :
            pass

        try:
            if "HTTP/1" in clipboard_content:
                data=all(clipboard_content)
                #scheme, host, int(port), path,method,body,headers,Cookie
                scheme=data[0]
                host=data[1].strip()
                # print(scheme,host)
                port=data[2].strip()
                path=data[3]

                method=data[4]
                body=data[5].strip()
                headers=data[6]
                Cookie=data[7].strip()
                # print(scheme, host, port, path,method,body,headers,Cookie)
                if method =="POST":
                    self._请求方式.setCurrentIndex(1)
                if port=="443" or port=="80":
                    self._请求地址.setPlainText (f"{scheme}://{host}{path}")
                else:
                    self._请求地址.setPlainText (f"{scheme}://{host}:{port}{path}")
                
                headers_str = '\n'.join(f"{key}: {value}" for key, value in headers.items())
                self._提交的协议头.setPlainText(headers_str)
                self._提交的数据.setPlainText(body)
                self._提交的ck.setPlainText(Cookie)
                
            else:
                self._状态栏.showMessage(" 非法数据包！", 2000) 
                show_error_message(self," 非法数据包！")
        except Exception  as e:#Exception 
            print(e)
            pass
    def c(self):
        print("_发送 \n")    #method,url,data,headers,cookies,proxies
        proxy_ip= self._代理地址.text() 
        url=self._请求地址.toPlainText() 
        method=self._请求方式.currentText() 
        data=self._提交的数据.toPlainText()
        headers=self._提交的协议头.toPlainText()
        cookies=self._提交的ck.toPlainText()
        """
        处理格式
        """
        headers_dict = {}
        lines = headers.strip().split('\n')
        for line in lines:
            if line.strip():  # 确保行不是空的
                key, value = line.split(':', 1)  # 分割一次，以处理值中可能包含 : 的情况
                headers_dict[key.strip()] = value.strip()


        sysprox= self._禁止重定向.isChecked()
        proxies=None
        if self._使用系统代理.isChecked() or  proxy_ip !="":
            try:
                ip = read_config('app.ini', 'Server', 'ip')
                name = read_config('app.ini', 'Server', 'name')
                pwd = read_config('app.ini', 'Server', 'pwd')
            except Exception  as e:#Exception 
                print(e)
            proxies = {
                'http': f'http://{name}:{pwd}@{ip}',
                'https': f'http://{name}:{pwd}@{ip}',
                }
        else:
            if proxy_ip !="" :
                proxies = {
                    'http': f'http://{proxy_ip}',
                    'https': f'http://{proxy_ip}',
                }

        # print(proxies)
        self._状态栏.showMessage("发送中...",0) 
        # 创建线程对象
        self.thread = RequestThread(url,method,data,headers_dict,cookies,proxies)
        # 连接线程的信号到槽函数，用于接收结果
        self.thread.result_signal.connect(self.on_request_finished)
        # 启动线程
        self.thread.start()

    def d(self):
        if self._使用系统代理.isChecked() :
            self.ss=MainWindows()
            self.ss.show()
            self._状态栏.showMessage(" 请设置/核对-代理地址及账号密码！", 5000)
    def show_status_message(self):
        # 在状态栏上显示一条消息
        self._状态栏.showMessage(" 按钮被点击了！", 2000)  # 消息显示2秒

    def on_request_finished(self, data):
        # 线程完成，更新 UI
        print("请求结果:", data)
        
        # 可以在这里添加代码更新状态栏或其他 UI 元素
        if "status_code" in data:
            
            self._响应正文.setPlainText(data["text"])
            headers_str = '\n'.join(f'{key}: {value}' for key, value in data["headers"].items())
            self._返回的协议头.setPlainText(headers_str)
            cookies_str = '\n'.join(f'{key}: {value}' for key, value in data["cookies"].items())
            self._返回的cookies.setPlainText(cookies_str)
            self._状态栏.showMessage(f"状态码：{str(data['status_code'])}  发送成功:)", 0) 
        else:
            self._状态栏.showMessage(f"发送失败:( {str(data)}", 0)     

    # 引入第二个窗口
    # def a(self):
    #     self.ss=MainWindows()
    #     self.ss.show()


# 加载第二个窗口
class MainWindows(QDialog):
    def __init__(self) -> None:
        super().__init__()
        # uic.loadUi("2.ui",self)
        self.ui = Ui_Form()  # 创建 UI 类的实例
        self.ui.setupUi(self)
        self.__box()#注册控件
      
        self.__app()#启动功能/事件

    def __box(self):    
        self._代理地址: QLineEdit=self.ui.lineEdit
        self._用户名: QLineEdit=self.ui.lineEdit_2
        self._密码: QLineEdit=self.ui.lineEdit_3
    

    def __app(self):
        try:
            ip = read_config('app.ini', 'Server', 'ip')
            name = read_config('app.ini', 'Server', 'name')
            pwd = read_config('app.ini', 'Server', 'pwd')
            self._代理地址.setText(ip)
            self._用户名.setText(name)
            self._密码.setText(pwd)
        except Exception  as e:#Exception 
            print(e)

    def closeEvent(self, event):  # 重写 closeEvent 方法
        print("对话框即将关闭")
        settings={}
        settings["ip"]=self._代理地址.text()
        settings["name"]=self._用户名.text()
        settings["pwd"]=self._密码.text()
        save_config('app.ini', 'Server', settings)

        # 如果需要取消关闭，调用 event.ignore() 而不是 event.accept()
        # event.ignore()
        super().closeEvent(event)  # 调用父类的 closeEvent 以确保正常关闭


if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec())

