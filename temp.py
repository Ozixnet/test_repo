```Python
import time
import random
import matplotlib.pyplot as plt

class NTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def find_path_to_root(node, parent_map):
    """Функция для нахождения пути от узла до корня (включая сам узел)."""
    path = []
    while node:
        path.append(node)
        node = parent_map.get(node)  # Получаем родителя узла
    return path

def lowest_common_ancestor(root, nodes):
    """Нахождение общего предка для M узлов в N-арном дереве."""
    if not nodes:
        return None

    # Создадим карту родительских узлов для поиска пути от узлов до корня
    parent_map = {}

    # Функция для обхода дерева и построения parent_map
    def dfs(node, parent=None):
        parent_map[node] = parent
        for child in node.children:
            dfs(child, node)

    # Строим parent_map для всего дерева
    dfs(root)

    # Находим пути для каждого из узлов
    paths = [find_path_to_root(node, parent_map) for node in nodes]

    # Ищем наибольший общий префикс среди путей
    min_length = min(len(path) for path in paths)
    common_ancestor = None

    for i in range(min_length):
        current_nodes = {path[i] for path in paths}
        if len(current_nodes) == 1:  # Если все узлы одинаковы на этой глубине
            common_ancestor = paths[0][i]
        else:
            break

    return common_ancestor

def build_random_n_ary_tree(num_nodes, max_children):
    """Строит случайное N-арное дерево с заданным количеством узлов и максимальным числом потомков."""
    nodes = [NTreeNode(i) for i in range(num_nodes)]
    for i in range(1, num_nodes):
        parent = random.choice(nodes[:i])  # Выбираем случайного родителя из уже созданных узлов
        parent.children.append(nodes[i])
    return nodes[0], nodes

def measure_execution_time(tree_size, max_children, num_queries):
    """Измеряет время выполнения для дерева заданного размера."""
    root, nodes = build_random_n_ary_tree(tree_size, max_children)
    query_nodes = random.sample(nodes, num_queries)

    start_time = time.time()
    lowest_common_ancestor(root, query_nodes)
    end_time = time.time()

    return end_time - start_time

def calculate_tree_height(root):
    """Вычисляет высоту дерева."""
    if not root.children:
        return 1
    return 1 + max(calculate_tree_height(child) for child in root.children)

# Параметры для тестирования
sizes = [10, 50, 100, 500, 1000, 5000, 10000]  # Различные размеры деревьев
max_children = 5  # Максимальное количество потомков
num_queries = 5  # Количество узлов, для которых ищем общего предка

theoretical_times = []
practical_times = []

# Теоретическое время (O(M * H))
def theoretical_time(height, num_queries):
    return num_queries * height

for size in sizes:
    root, _ = build_random_n_ary_tree(size, max_children)
    height = calculate_tree_height(root)  # Точная высота дерева
    theoretical_times.append(theoretical_time(height, num_queries))

    # Практическое измерение времени
    practical_time = measure_execution_time(size, max_children, num_queries)
    practical_times.append(practical_time)

# Нормализация теоретических данных для согласования масштаба
scale_factor = max(practical_times) / max(theoretical_times)
theoretical_times = [t * scale_factor for t in theoretical_times]

# Построение графиков
plt.figure(figsize=(10, 6))
plt.plot(sizes, theoretical_times, label="Теоретическое время (нормализовано)", marker="o")
plt.plot(sizes, practical_times, label="Практическое время", marker="o")
plt.xlabel("Размер дерева (количество узлов)")
plt.ylabel("Время выполнения (секунды)")
plt.title("Сравнение теоретического и практического времени выполнения")
plt.legend()
plt.grid()
plt.show()
```