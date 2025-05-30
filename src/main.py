from src.graph_loader import load_graph
from src.genetic_algorithm import run_ga
from src.visualizer import draw_graph
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    filename = "gc_50_9"  # <--- farklı data testleri için burayı değiştircezz!
    data_path = f"../data/{filename}.txt"
    result_txt_path = f"../results/{filename}_result.txt"
    result_img_path = f"../results/{filename}_plot.png"

    num_nodes, edges = load_graph(data_path)
    solution = run_ga(num_nodes, edges)
    used_colors = len(set(solution))

    # ⬇️ 1. METİN SONUCU KAYDET
    os.makedirs("../results", exist_ok=True)
    with open(result_txt_path, "w") as f:
        f.write(f"Minimum Colors Used: {used_colors}\n")
        f.write("Color Assignment:\n")
        f.write(" ".join(map(str, solution)) + "\n")

    # ⬇️ 2. GRAFİĞİ KAYDET
    plt.figure()
    draw_graph(num_nodes, edges, solution)
    plt.savefig(result_img_path, dpi=300)
    plt.close()

    # ⬇️ 3. Terminale yaz
    print(f"\n🎨 Minimum Colors Used: {used_colors}")
    print("Color Assignment:", solution)
    print(f"\n📁 Sonuçlar kaydedildi: {result_txt_path}, {result_img_path}")
