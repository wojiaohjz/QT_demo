from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTableWidgetItem
import requests

uiloader = QUiLoader()


class Postman:

    def __init__(self):
        self.ui = uiloader.load("ui/postman.ui")

        self.ui.methodSelect.addItems(["GET", "POST", "PUT", "DELETE"])
        self.ui.methodSelect.currentIndexChanged.connect(self.handleMethodChange)
        self.method = self.ui.methodSelect.currentText()

        self.ui.urlEdit.setPlaceholderText('请在这里输入URL')
        self.url = self.ui.urlEdit.text()
        self.ui.urlEdit.textChanged.connect(self.handleUrlChange)

        self.headers = {}
        self.headers_num = 0
        # 设定第1列的宽度为 180像素
        self.ui.headersTable.setColumnWidth(0, 100)
        # 设定第2列的宽度为 100像素
        self.ui.headersTable.setColumnWidth(1, 120)
        self.ui.insert_headers_button.clicked.connect(self.handleInsertHeadersButtonClick)
        self.ui.delete_headers_button.clicked.connect(self.handleDeleteHeadersButtonClick)
        self.ui.headersTable.cellChanged.connect(self.cfgItemChanged)

        self.ui.bodyEdit.setPlaceholderText('请在这里输入请求体')
        self.body = self.ui.bodyEdit.toPlainText()
        self.ui.bodyEdit.textChanged.connect(self.handleBodyChange)

        self.ui.sendButton.clicked.connect(self.handleSendButtonClick)

    def handleMethodChange(self):
        self.method = self.ui.methodSelect.currentText()

    def handleUrlChange(self):
        self.url = self.ui.urlEdit.text()

    def handleInsertHeadersButtonClick(self):
        self.ui.headersTable.insertRow(self.headers_num)
        self.ui.headersTable.setItem(self.headers_num, 0, QTableWidgetItem('key'))
        self.ui.headersTable.setItem(self.headers_num, 1, QTableWidgetItem('value'))
        self.updateHeaders()
        self.headers_num += 1

    def handleDeleteHeadersButtonClick(self):
        if self.headers_num > 0:
            self.ui.headersTable.removeRow(self.headers_num - 1)
            self.headers_num -= 1
            self.updateHeaders()

    def cfgItemChanged(self, row, column):
        self.updateHeaders()

    def updateHeaders(self):
        rowcount = self.ui.headersTable.rowCount()
        self.headers.clear()
        for i in range(rowcount):
            key = self.ui.headersTable.item(i, 0).text()
            value = self.ui.headersTable.item(i, 1).text()
            self.headers[key] = value
        # print(self.headers)

    def handleBodyChange(self):
        self.body = self.ui.bodyEdit.toPlainText()

    def handleSendButtonClick(self):
        print(f"method: {self.method}")
        print(f"url: {self.url}")
        print(f"headers: {self.headers}")
        print(f"body: {self.body}")
        response = requests.request(self.method, self.url, headers=self.headers, data=self.body)
        self.ui.textBrowser.append("******response******")
        self.ui.textBrowser.append(f"status code: {response.status_code}")
        self.ui.textBrowser.append(f"headers: {response.headers}")
        self.ui.textBrowser.append(f"body: {response.content.decode('utf-8')}")
        self.ui.textBrowser.ensureCursorVisible()


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('logo.png'))
    postman = Postman()
    postman.ui.show()
    app.exec()
