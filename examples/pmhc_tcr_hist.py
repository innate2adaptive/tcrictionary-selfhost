import matplotlib.pyplot as plt
import seaborn as sns
from neo4j import GraphDatabase

sns.set_theme()

driver = GraphDatabase.driver("bolt://localhost:7687")

with driver.session() as session:
    result = session.run(
        """
        MATCH (tcr:Tcr)--(:Annotation)--(pmhc:PMhc)
        WITH pmhc, count(DISTINCT tcr) AS tcr_count
        RETURN tcr_count
    """
    )

    tcr_counts = [record["tcr_count"] for record in result]

driver.close()

print(f"Number of pMHCs with at least one TCR: {len(tcr_counts):,}")
print(f"Max TCRs per pMHC: {max(tcr_counts) if tcr_counts else 0}")
print(f"Min TCRs per pMHC: {min(tcr_counts) if tcr_counts else 0}")

fig, ax = plt.subplots(figsize=(8, 4))

sns.histplot(
    tcr_counts,
    bins=50,
    ax=ax,
    color="#ffc078",
    log_scale=True,
)

ax.set_xlabel("Number of unique TCRs per pMHC")
ax.set_ylabel("Number of pMHCs")
ax.set_yscale("log")
ax.set_xlim(left=1)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig("pmhc_tcr_degree_histogram.svg")

plt.show()

print("\n" + "=" * 50)
print("Histogram complete!")
print("=" * 50)

