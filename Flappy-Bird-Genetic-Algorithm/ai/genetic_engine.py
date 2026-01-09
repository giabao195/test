from objects.bird import Bird
import numpy as np


def mutate(weights, mutation_prob=0.5):
    """
    Đột biến một trọng số dựa trên yếu tố ngẫu nhiên.
    :param mutation_prob: Xác suất đột biến (mặc định 0.5).
    :param weights: Các ma trận trọng số (weights) hoặc bias cần đột biến.
    :return: Trọng số đã đột biến.
    """
    # Tạo mặt nạ (mask) ngẫu nhiên: 1 nếu xảy ra đột biến, 0 nếu không
    mask = (np.random.rand(*weights.shape) < mutation_prob).astype(int)

    # Tạo giá trị đột biến: random sign (+/- 1) * random magnitude
    mutation = (np.random.choice([-1, 1], size=weights.shape)
                * np.random.randint(0, 30) * 0.0005)

    # Tính toán trọng số đã đột biến (áp dụng mutation chỉ ở những vị trí mask là 1)
    return weights + mask * mutation


def clone_brain(bird):
    """
    Sao chép (clone) một con chim và thực hiện đột biến gene nhẹ trên bản sao.
    :param bird: Chim cần sao chép.
    :return: Con chim mới (đã đột biến nhẹ).
    """
    # Tạo một con chim mới (giữ nguyên gene)
    new_bird = bird.clone()

    # Thực hiện đột biến gene trên các tham số của bộ não
    new_bird.brain.receive_genes(
        W1=mutate(bird.brain.W1),
        b1=mutate(bird.brain.b1),
        W2=mutate(bird.brain.W2),
        b2=mutate(bird.brain.b2),
    )

    return new_bird


def combine_brain(bird_mom: Bird, bird_dad: Bird):
    """
    Kết hợp bộ não của chim mẹ và chim bố để tạo ra chim con mới (Crossover).
    Gene được lấy trung bình từ bố và mẹ, sau đó đột biến nhẹ.
    :param bird_mom: Chim mẹ (cá thể có điểm cao).
    :param bird_dad: Chim bố (cá thể có điểm cao).
    :return: Một con chim mới là sự kết hợp của bố và mẹ.
    """
    # Tạo một con chim mới
    bird = Bird()

    # Tiến hành kết hợp bộ não (Crossover)
    # mom_score = bird_mom.score
    # dad_score = bird_dad.score

    # Tính toán tỉ lệ kết hợp (Hiện tại là 50/50, có thể thay đổi dựa trên điểm số)
    mom_ratio = 0.5
    dad_ratio = 0.5

    # Kết hợp các tham số (trọng số/bias) bằng cách lấy trung bình
    child_W1 = mom_ratio * bird_mom.brain.W1 + dad_ratio * bird_dad.brain.W1
    child_W2 = mom_ratio * bird_mom.brain.W2 + dad_ratio * bird_dad.brain.W2
    child_b1 = mom_ratio * bird_mom.brain.b1 + dad_ratio * bird_dad.brain.b1
    child_b2 = mom_ratio * bird_mom.brain.b2 + dad_ratio * bird_dad.brain.b2

    # Nhận gene đã lai tạo và thực hiện đột biến nhẹ ngay lập tức
    bird.brain.receive_genes(
        W1=mutate(child_W1),
        b1=mutate(child_b1),
        W2=mutate(child_W2),
        b2=mutate(child_b2)
    )

    return bird


def breed_bird(bird_mom: Bird, bird_dad: Bird, num_children: int):
    """
    Tạo ra một danh sách chim con bằng cách lai tạo bộ não của hai chim bố mẹ.
    :param bird_mom: Chim mẹ.
    :param bird_dad: Chim bố.
    :param num_children: Số lượng chim con cần sinh ra.
    :return: Danh sách các chim con mới.
    """
    return [combine_brain(bird_mom, bird_dad) for _ in range(num_children)]


def clone_bird(bird: Bird, num_children: int):
    """
    Sao chép chim thành nhiều cá thể con, mỗi cá thể đều có đột biến nhẹ (mutation).
    :param bird: Chim cần sao chép.
    :param num_children: Số lượng chim con cần sinh ra.
    :return: Danh sách các chim con đã sao chép.
    """
    return [clone_brain(bird) for _ in range(num_children)]


