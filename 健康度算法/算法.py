import numpy as np

# 报警扣分
P = [0, 10, 100, 1000]  # P[1]=10, P[2]=100, P[3]=1000，P[0]不用

def calculate_score(A, N, M):
    """
    A: shape = (3, N, M)，A[p-1, j, t] 表示第t分钟第j项p级报警（p=1,2,3），可以为次数
    N: 测项总数
    M: 总观测分钟数
    """
    # 只要出现过就算1，否则0
    A = (A > 0).astype(int)
    # 计算每个测项每分钟的扣分
    D_jt = P[1] * A[0] + P[2] * A[1] + P[3] * A[2]  # shape = (N, M)
    # 计算每分钟总扣分
    D_t = np.sum(D_jt, axis=0)  # shape = (M,)
    # 每分钟得分
    S_t = N - D_t
    # 百分制折算得分
    S_t_prime = S_t / N
    # 平均折算得分
    S_prime_avg = np.mean(S_t_prime)
    # 最终得分
    S_display = max(0, round(100 * S_prime_avg))
    return S_display

def calculate_daily_scores(A, N, minutes_per_day=1440):
    """
    A: shape = (3, N, M_total)
    N: 测项总数
    minutes_per_day: 一天的分钟数，默认1440
    返回：每天的得分列表
    """
    M_total = A.shape[2]
    num_days = M_total // minutes_per_day
    scores = []
    for day in range(num_days):
        start = day * minutes_per_day
        end = start + minutes_per_day
        A_day = A[:, :, start:end]
        score = calculate_score(A_day, N, minutes_per_day)
        scores.append(score)
    return scores

# 示例：假设有2天的数据
N = 5
days = 2
minutes_per_day = 10  # 为了演示，假设一天10分钟
M_total = days * minutes_per_day
np.random.seed(0)
A = np.random.randint(0, 2, size=(3, N, M_total))

daily_scores = calculate_daily_scores(A, N, minutes_per_day)
for i, s in enumerate(daily_scores, 1):
    print(f"第{i}天的最终得分: {s}")
