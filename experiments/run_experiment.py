import argparse, statistics, pathlib, yaml, json
from gcp.draw_solution import draw_graph  # 🔄 yeni: çözüm grafiği çizimi için eklendi

import pandas as pd
import matplotlib.pyplot as plt

from ga.engine import GAEngine
from gcp.graph import Graph

CFG = yaml.safe_load(open("config.yaml"))

# ---------------------------------------------------- #
def one_run(instance: str) -> tuple:
    g  = Graph(instance)
    ga = GAEngine(g, CFG)
    stats = ga.run()                     # stats["best_fit"] list
    best_curve = stats["best_fit"]
    best_individual = ga.pop.best()[0]  # 🔄 yeni: çözüm objesi alınıyor
    return best_curve, min(best_curve), best_individual

# ---------------------------------------------------- #
def main(instance_path: str, show: bool):
    stem = pathlib.Path(instance_path).stem       # gc_70_9
    runs = CFG["runs"]

    all_curves, final_vals, best_inds = [], [], []  # 🔄 yeni: en iyi bireyler de tutuluyor
    for r in range(runs):
        curve, best_val, best_ind = one_run(instance_path)
        all_curves.append(curve)
        final_vals.append(best_val)
        best_inds.append(best_ind)


    gen_len = len(all_curves[0])
    avg_curve = [
        statistics.mean(all_curves[r][g] for r in range(runs))
        for g in range(gen_len)
    ]
    avg_best = statistics.mean(final_vals)


    out_xlsx = pathlib.Path("../visuals") / f"{stem}_result.xlsx"
    df = pd.DataFrame({
        "Run": list(range(1, runs + 1)),
        "BestFitness": final_vals
    })
    df.loc[runs, ["Run", "BestFitness"]] = ["AVG", avg_best]
    df.to_excel(out_xlsx, index=False)
    print(f"[✓] Sonuç yazıldı → {out_xlsx}")

    plt.plot(avg_curve, label="Avg Best Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title(f"{stem}  (avg best ≈ {avg_best:.2f})")
    plt.legend()
    out_png = out_xlsx.with_name(f"{stem}_conv.png")
    plt.savefig(out_png, dpi=150)
    if show:
        plt.show()
    plt.close()

    out_json = out_xlsx.with_name(f"{stem}_runs.json")
    json.dump(all_curves, open(out_json, "w"))

    # 🔄 yeni: çözüm grafiğini çiz
    best_idx = final_vals.index(min(final_vals))
    best_sol = best_inds[best_idx]
    out_graph = out_xlsx.with_name(f"{stem}_graph.png")
    draw_graph(instance_path, best_sol.colors, save_path=out_graph)
    print(f"[✓] Çözüm grafiği çizildi → {out_graph}")

# ---------------------------------------------------- #
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("instance", nargs="?", default="../data/gc_70_9.txt")
    p.add_argument("--show", action="store_true")
    args = p.parse_args()
    main(args.instance, args.show)
