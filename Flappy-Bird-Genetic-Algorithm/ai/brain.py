import numpy as np


def sigmoid(x):
    """
    Tính hàm Sigmoid của vector x.
    Sigmoid thường dùng để giới hạn đầu ra trong khoảng (0, 1).
    :param x: Một vector (numpy array).
    :return: Giá trị Sigmoid của x.
    """
    return 1 / (1 + np.exp(-x))

                        
def relu(x):
    """
    Tính hàm ReLU (Rectified Linear Unit) của vector x.
    ReLU giúp mạng nơ-ron học phi tuyến tính và thường dùng trong các lớp ẩn.
    :param x: Một vector (numpy array).
    :return: Giá trị ReLU của x (max(0, x)).
    """
    return x * (x > 0)


class Brain:
    """Đại diện cho mạng nơ-ron nhân tạo (Neural Network) 2 lớp của chim."""
    def __init__(self):
        # Khởi tạo ma trận trọng số (W) và bias (b) cho Lớp Ẩn 1
        # Kích thước W1: (5 đầu vào, 2 nơ-ron)
        self.W1 = np.random.normal(loc=0, scale=0.1, size=(5, 2))
        self.b1 = np.random.normal(loc=0, scale=0.1, size=(2,))

        # Khởi tạo ma trận trọng số (W) và bias (b) cho Lớp Đầu ra 2
        # Kích thước W2: (2 đầu vào, 1 đầu ra)
        self.W2 = np.random.normal(loc=0, scale=0.1, size=(2, 1))
        self.b2 = np.random.normal(loc=0, scale=0.1, size=(1,))

    def perform_action(self, vision):
        """
        Thực hiện tính toán truyền xuôi (Feedforward) qua mạng nơ-ron để đưa ra quyết định.
        :param vision: Vector numpy (5 phần tử) thông tin đầu vào của chim (vision).
        :return: True nếu chim nên "flap" (nhảy), ngược lại False.
        """
        # Tính toán Lớp 1 (Lớp Ẩn): Output = Sigmoid(Vision . W1 + b1)
        output = sigmoid(np.dot(vision, self.W1) + self.b1)
        # Tính toán Lớp 2 (Lớp Đầu ra): Output = Sigmoid(Output_L1 . W2 + b2)
        output = sigmoid(np.dot(output, self.W2) + self.b2)
        
        # Quyết định hành động: Nếu giá trị đầu ra >= 0.5 thì chim nhảy
        return output[0] >= 0.5

    def receive_genes(self, W1, b1, W2, b2):
        """
        Nhận gene (trọng số và bias) từ các cá thể bố mẹ trong quá trình nhân bản/lai tạo.
        :param W1: Ma trận trọng số lớp 1.
        :param b1: Vector bias lớp 1.
        :param W2: Ma trận trọng số lớp 2.
        :param b2: Vector bias lớp 2.
        :return: None
        """
        # Cập nhật các trọng số và bias
        self.W1 = W1
        self.b1 = b1
        self.W2 = W2
        self.b2 = b2

        