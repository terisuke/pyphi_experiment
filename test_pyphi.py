import pyphi
import numpy as np
import multiprocessing

print(f"PyPhi version: {pyphi.__version__}")

def run_pyphi_test():
    # 簡単な2ノードシステムの例（XORゲート）
    # 状態: (0, 0), (0, 1), (1, 0), (1, 1)
    # ノード A, B
    # 次の状態 t+1 は現在の状態 t に依存
    # 例：A(t+1) = A(t) XOR B(t), B(t+1) = B(t)

    # 遷移確率行列 (TPM) - state-by-node form
    # 各行は現在の状態（00, 01, 10, 11）を表す
    # 各列は次の状態でのノードの値（A, B）を表す
    tpm = np.array([
        [0, 0],  # 00 -> 00
        [1, 1],  # 01 -> 11
        [1, 0],  # 10 -> 10
        [0, 1],  # 11 -> 01
    ])

    # TPMを2次元から3次元に変換（PyPhi 1.2.0の形式）
    tpm = pyphi.convert.state_by_node2state_by_state(tpm)

    # (オプション) 接続行列 (CM) - 全結合を仮定しない場合
    # A -> A, B -> A, B -> B
    cm = np.array([
        [1, 1], # Aへの入力 (Aから, Bから) - XORなので両方から影響
        [0, 1]  # Bへの入力 (Aから, Bから) - BはB自身からのみ影響
    ])

    labels = ('A', 'B')

    try:
        network = pyphi.Network(tpm, cm=cm, node_labels=labels)
        print("Network object created successfully:")
        print(network)

        # 簡単なサブシステム (現在の状態を定義)
        state = (0, 0) # 例: A=0, B=0（最も単純な状態から始める）
        subsystem = pyphi.Subsystem(network, state)
        print("\nSubsystem object created successfully for state", state)
        print(subsystem)

        # ===== 統合情報理論(IIT)のφ値計算 =====
        print("\n===== 統合情報理論(IIT)のφ値計算 =====")
        
        # システムのφ値を計算
        phi = pyphi.compute.phi(subsystem)
        print(f"システム全体のφ値: {phi}")
        
        # 各ノードのφ値を計算（修正版7）
        print("\n各ノードのφ値:")
        for i in range(network.size):
            # 単一ノードのサブシステムを作成
            node_subsystem = pyphi.Subsystem(network, state, (i,))
            try:
                node_phi = pyphi.compute.phi(node_subsystem)
                print(f"ノード {labels[i]}: φ = {node_phi}")
            except Exception as e:
                print(f"ノード {labels[i]}のφ値計算中にエラー: {e}")
        
        # 異なる状態でのφ値の比較
        print("\n異なる状態でのφ値の比較:")
        test_states = [(0, 0), (0, 1), (1, 0), (1, 1)]  # 全ての可能な状態をテスト
        for s in test_states:
            try:
                s_subsystem = pyphi.Subsystem(network, s)
                s_phi = pyphi.compute.phi(s_subsystem)
                print(f"状態 {s}: φ = {s_phi}")
            except Exception as e:
                print(f"状態 {s}のφ値計算中にエラー: {e}")
        
        # ===== 3ノードシステムの例 =====
        print("\n===== 3ノードシステムの例 =====")
        
        # 3ノードのTPM - state-by-node form
        # より複雑な相互作用を持つシステム
        # 各ノードは他の2つのノードからの入力を受け取る
        # ノードの次の状態は、入力の多数決で決まる
        tpm_3node = np.array([
            [0, 0, 0],  # 000 -> 000 (全てのノードが0なら次も0)
            [0, 0, 1],  # 001 -> 001 (1つだけ1なら状態を維持)
            [0, 1, 0],  # 010 -> 010 (1つだけ1なら状態を維持)
            [0, 1, 1],  # 011 -> 011 (2つ1なら状態を維持)
            [1, 0, 0],  # 100 -> 100 (1つだけ1なら状態を維持)
            [1, 0, 1],  # 101 -> 101 (2つ1なら状態を維持)
            [1, 1, 0],  # 110 -> 110 (2つ1なら状態を維持)
            [1, 1, 1],  # 111 -> 111 (全て1なら1のまま)
        ])

        # TPMを3次元に変換
        tpm_3node = pyphi.convert.state_by_node2state_by_state(tpm_3node)

        # 3ノードの接続行列 - 全結合
        cm_3node = np.array([
            [1, 1, 1],  # ノード0は全てのノードから入力を受ける
            [1, 1, 1],  # ノード1は全てのノードから入力を受ける
            [1, 1, 1]   # ノード2は全てのノードから入力を受ける
        ])

        labels_3node = ('X', 'Y', 'Z')
        network_3node = pyphi.Network(tpm_3node, cm=cm_3node, node_labels=labels_3node)

        # 異なる初期状態でのφ値を計算
        print("\n3ノードシステムの異なる状態でのφ値:")
        test_states_3node = [
            (0, 0, 0),  # 全て0
            (0, 0, 1),  # 1つだけ1
            (0, 1, 1),  # 2つ1
            (1, 1, 1)   # 全て1
        ]

        for s in test_states_3node:
            try:
                subsystem_3node = pyphi.Subsystem(network_3node, s)
                phi_3node = pyphi.compute.phi(subsystem_3node)
                print(f"状態 {s}: φ = {phi_3node}")
            except Exception as e:
                print(f"状態 {s}のφ値計算中にエラー: {e}")

        print("\nPyPhi seems to be installed and working correctly!")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your installation and the example code.")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    run_pyphi_test()