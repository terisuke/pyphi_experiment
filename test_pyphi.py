import pyphi
import numpy as np

print(f"PyPhi version: {pyphi.__version__}")

# 簡単な2ノードシステムの例（XORゲート）
# 状態: (0, 0), (0, 1), (1, 0), (1, 1)
# ノード A, B
# 次の状態 t+1 は現在の状態 t に依存
# 例：A(t+1) = A(t) XOR B(t), B(t+1) = B(t)

# 遷移確率行列 (TPM) - state-by-node deterministic form
# 各行: 現在の状態 (00, 01, 10, 11)
# 各列: 次のタイムステップでの各ノードの値 (A(t+1), B(t+1))
tpm = np.array([
    [0, 0],  # 現在 00 -> 次 00 (0^0=0, B=0)
    [1, 1],  # 現在 01 -> 次 11 (0^1=1, B=1)
    [1, 0],  # 現在 10 -> 次 10 (1^0=1, B=0)
    [0, 1]   # 現在 11 -> 次 01 (1^1=0, B=1)
])

# (オプション) 接続行列 (CM) - 全結合を仮定しない場合
# A -> A, B -> A, B -> B
cm = np.array([
    [1, 1], # Aへの入力 (Aから, Bから) - XORなので両方から影響
    [0, 1]  # Bへの入力 (Aから, Bから) - BはB自身からのみ影響
])

labels = ('A', 'B')

# Networkオブジェクトの作成
try:
    network = pyphi.Network(tpm, cm=cm, node_labels=labels)
    print("Network object created successfully:")
    print(network)

    # 簡単なサブシステム (現在の状態を定義)
    state = (1, 0) # 例: A=1, B=0
    subsystem = pyphi.Subsystem(network, state)
    print("\nSubsystem object created successfully for state", state)
    print(subsystem)

    print("\nPyPhi seems to be installed and working correctly!")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please check your installation and the example code.")