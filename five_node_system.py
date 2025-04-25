import numpy as np
import pyphi
import os

# PyPhiのウェルカムメッセージを抑制
os.environ['PYPHI_WELCOME_OFF'] = 'yes'

class FiveNodeSystem:
    def __init__(self):
        # TPMの初期化
        self.tpm = np.zeros((32, 5))  # state-by-node形式
        self._initialize_tpm()
        self.network = self._create_network()

    def _initialize_tpm(self):
        # 非線形な状態遷移を実装
        # 全ての可能な状態に対してTPMを定義
        for i, state in enumerate(self._generate_all_states()):
            next_state = self._compute_next_state(state)
            self.tpm[i] = next_state

    def _generate_all_states(self):
        # 全ての可能な状態（2^5 = 32通り）を生成
        return [(i >> 4 & 1, i >> 3 & 1, i >> 2 & 1, i >> 1 & 1, i & 1) 
                for i in range(32)]

    def _compute_next_state(self, state):
        # 非線形な状態遷移ルールを定義
        n1, n2, n3, n4, n5 = state
        
        # より複雑な相互作用を実装
        next_n1 = (n2 and n3) or (n4 and n5)  # ノード1は2&3または4&5が活性化している場合に活性化
        next_n2 = n1 or (n3 and n4)           # ノード2は1が活性化しているか、3&4が活性化している場合に活性化
        next_n3 = (n1 and n2) or n5           # ノード3は1&2または5が活性化している場合に活性化
        next_n4 = n3 or (n1 and n5)           # ノード4は3が活性化しているか、1&5が活性化している場合に活性化
        next_n5 = (n2 and n4) or n3           # ノード5は2&4または3が活性化している場合に活性化
        
        return np.array([next_n1, next_n2, next_n3, next_n4, next_n5])

    def _create_network(self):
        try:
            # ネットワークの作成
            network = pyphi.Network(self.tpm)
            return network
        except Exception as e:
            print(f"ネットワーク作成エラー: {e}")
            raise

    def compute_phi(self, state):
        try:
            # 指定された状態のΦ値を計算
            subsystem = pyphi.Subsystem(self.network, state)
            return pyphi.compute.phi(subsystem)
        except Exception as e:
            print(f"Φ値計算エラー: {e}")
            return 0.0  # エラー時は0を返す

    def get_next_state(self, state):
        try:
            # 状態のインデックスを計算
            index = sum(v * (2 ** (4-i)) for i, v in enumerate(state))
            return tuple(self.tpm[index].astype(int))
        except Exception as e:
            print(f"次の状態計算エラー: {e}")
            return state  # エラー時は現在の状態を返す

# テスト用のコード
if __name__ == '__main__':
    try:
        system = FiveNodeSystem()
        
        # 特定の状態のΦ値を計算
        test_states = [
            (0, 1, 1, 1, 1),
            (1, 1, 1, 1, 1)
        ]
        
        for state in test_states:
            phi = system.compute_phi(state)
            print(f"State {state}: Φ = {phi}")
    except Exception as e:
        print(f"テストエラー: {e}") 