import yaml, json, pathlib
from datetime import datetime
import matplotlib.pyplot as plt

from gcp.graph import Graph
from ga.engine import GAEngine

CFG = yaml.safe_load(open("config.yaml"))

def main(instance_path: str):
    g = Graph(instance_path)
    ga = GAEngine(g, CFG)
    stats = ga.run()

    # save stats
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = pathlib.Path("../visuals") / f"run_{ts}"
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    # plot convergence
    plt.plot(stats["best_fit"], label="best")
    plt.plot(stats["avg_fit"], label="avg")
    plt.xlabel("generation")
    plt.ylabel("fitness")
    plt.legend()
    plt.title(instance_path)
    plt.savefig(out_dir / "convergence.png", dpi=150)
    plt.close()

if __name__ == "__main__":
    main("../data/gc_100_9.txt")
