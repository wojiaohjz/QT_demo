from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox
from socket import *
from traceback import format_exc

uiloader = QUiLoader()


class ProtocolTest:

    def __init__(self):
        self.ui = uiloader.load("ui/protocol_test.ui")

        self.ui.listWidget.itemSelectionChanged.connect(self.handleItemSelectionChanged)

        self.ui.btn_connect_server.clicked.connect(self.handleConnectServerButtonClick)

        self.ui.btn_set_state.clicked.connect(self._set_machine_state)
        self.msg_id = 0

    def handleItemSelectionChanged(self):
        current_item = self.ui.listWidget.currentItem()
        if current_item is not None:
            item_text = current_item.text()
            match item_text:
                case "连接设备":
                    self.ui.stackedWidget.setCurrentIndex(0)
                case "设置风泵状态":
                    self.ui.stackedWidget.setCurrentIndex(1)
                case "获取风泵状态":
                    self.ui.stackedWidget.setCurrentIndex(2)
                case _:
                    QMessageBox.warning(
                        self.ui,
                        '警告',
                        '选择了未知的操作页面')

    def handleConnectServerButtonClick(self):
        ip = self.ui.lineEdit_ip.text()
        port = int(self.ui.lineEdit_port.text())
        buff_len = 1024
        # 实例化一个socket对象，指明协议
        self.dataSocket = socket(AF_INET, SOCK_STREAM)

        # 连接服务端socket
        try:
            self.dataSocket.connect((ip, port))
            self._log("连接成功")
        except:
            self._log(f"连接失败，错误信息：{format_exc()}")

    def _log(self, msg):
        self.ui.textBrowser.append(msg)
        self.ui.textBrowser.ensureCursorVisible()

    def _set_machine_state(self):
        try:
            dev_code = self.ui.input_code.text()
            dev_state = int(self.ui.input_state.text())
            body = b'\x01'
            if dev_code is not None:
                body += (len(dev_code) + 2).to_bytes(length=1, byteorder='big')
                body += dev_code.encode()
            if dev_state is not None:
                body += b'\x02\x03'
                body += dev_state.to_bytes(length=1, byteorder='big')
            header = b''
            header += (len(body) + 8).to_bytes(length=2, byteorder='big')
            header += b'\x02\xF0'
            self.msg_id += 1
            header += self.msg_id.to_bytes(length=4, byteorder='big')
            msg = header + body
            self.dataSocket.send(msg)
            self._log(f"发送消息：{msg.hex()}")
        except:
            self._log(f"设置风泵状态失败，错误信息：{format_exc()}")


if __name__ == '__main__':
    app = QApplication([])
    protocol_test = ProtocolTest()
    protocol_test.ui.show()
    # hex_data = bytes.fromhex("01 03 00 00 00 02 C4 0B")
    # print(hex_data, len(hex_data))
    app.exec()
