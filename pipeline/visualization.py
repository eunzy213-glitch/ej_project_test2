# pipeline/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns

def plot_removed_vs_kept(df_kept, df_removed, save_path):
    plt.figure(figsize=(6, 6))
    plt.scatter(df_kept["SG"], df_kept["BG"], alpha=0.3, label="Kept")
    plt.scatter(df_removed["SG"], df_removed["BG"], alpha=0.7, label="Removed", color="red")
    plt.legend()
    plt.xlabel("SG")
    plt.ylabel("BG")
    plt.title("Removed vs Kept Samples")
    plt.savefig(f"{save_path}/removed_vs_kept.png", dpi=300)
    plt.close()
