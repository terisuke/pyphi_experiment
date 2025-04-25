import sys
import os
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen
from five_node_system import FiveNodeSystem

# PyPhiのウェルカムメッセージを抑制
os.environ['PYPHI_WELCOME_OFF'] = 'yes'

class NodeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = 0
        self.setMinimumSize(50, 50)
        
    def setState(self, state):
        self.state = state
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # ノードの描画
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 3
        
        # 状態に応じて色を変更
        if self.state == 1:
            color = QColor(255, 100, 100)  # 活性化状態は赤
        else:
            color = QColor(200, 200, 200)  # 非活性化状態はグレー
            
        painter.setBrush(color)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(center, radius, radius)

class StateAnimationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.system = FiveNodeSystem()
            self.current_state = (0, 0, 0, 0, 0)
            self.initUI()
        except Exception as e:
            print(f"初期化エラー: {e}")
            sys.exit(1)
        
    def initUI(self):
        self.setWindowTitle('5ノードシステムの状態遷移アニメーション')
        self.setGeometry(100, 100, 800, 600)
        
        # メインウィジェットとレイアウト
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # ノードの表示用ウィジェット
        nodes_widget = QWidget()
        nodes_layout = QHBoxLayout(nodes_widget)
        self.node_widgets = []
        
        # 5つのノードを作成
        for i in range(5):
            node = NodeWidget()
            self.node_widgets.append(node)
            nodes_layout.addWidget(node)
            
        layout.addWidget(nodes_widget)
        
        # コントロールパネル
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # 開始状態の選択
        self.state_combo = QComboBox()
        self.state_combo.addItems([
            "00000", "00001", "00010", "00011", "00100",
            "00101", "00110", "00111", "01000", "01001",
            "01010", "01011", "01100", "01101", "01110",
            "01111", "10000", "10001", "10010", "10011",
            "10100", "10101", "10110", "10111", "11000",
            "11001", "11010", "11011", "11100", "11101",
            "11110", "11111"
        ])
        control_layout.addWidget(QLabel("初期状態:"))
        control_layout.addWidget(self.state_combo)
        
        # 制御ボタン
        self.start_button = QPushButton("開始")
        self.start_button.clicked.connect(self.start_animation)
        self.stop_button = QPushButton("停止")
        self.stop_button.clicked.connect(self.stop_animation)
        self.stop_button.setEnabled(False)
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        
        layout.addWidget(control_panel)
        
        # 状態表示ラベル
        self.state_label = QLabel("現在の状態: 00000")
        layout.addWidget(self.state_label)
        
        # Φ値表示ラベル
        self.phi_label = QLabel("Φ値: 0.0")
        layout.addWidget(self.phi_label)
        
        # エラーメッセージラベル
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)
        
        # タイマーの設定
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.animation_speed = 1000  # 1秒
        
    def start_animation(self):
        try:
            # 初期状態の設定
            initial_state = tuple(map(int, self.state_combo.currentText()))
            self.current_state = initial_state
            self.update_nodes()
            
            # アニメーション開始
            self.timer.start(self.animation_speed)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.error_label.setText("")
        except Exception as e:
            self.error_label.setText(f"エラー: {str(e)}")
        
    def stop_animation(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
    def update_state(self):
        try:
            # 次の状態を計算
            self.current_state = self.system.get_next_state(self.current_state)
            self.update_nodes()
        except Exception as e:
            self.error_label.setText(f"状態更新エラー: {str(e)}")
            self.stop_animation()
        
    def update_nodes(self):
        try:
            # 各ノードの状態を更新
            for i, node in enumerate(self.node_widgets):
                node.setState(self.current_state[i])
                
            # 状態とΦ値の表示を更新
            state_str = ''.join(map(str, self.current_state))
            self.state_label.setText(f"現在の状態: {state_str}")
            
            try:
                phi = self.system.compute_phi(self.current_state)
                self.phi_label.setText(f"Φ値: {phi:.6f}")
                self.error_label.setText("")
            except Exception as e:
                self.phi_label.setText("Φ値: 計算エラー")
                self.error_label.setText(f"Φ値計算エラー: {str(e)}")
        except Exception as e:
            self.error_label.setText(f"ノード更新エラー: {str(e)}")

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = StateAnimationWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"アプリケーションエラー: {e}")
        sys.exit(1) 