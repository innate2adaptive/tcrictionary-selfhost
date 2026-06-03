import matplotlib.pyplot as plt
import seaborn as sns
from neo4j import GraphDatabase

sns.set_theme()

driver = GraphDatabase.driver("bolt://localhost:7687")

queries = {
    r"Unique TCR-pMHCs": """
        MATCH (db:Database)--(:Study)--(:Annotation)--(tcr:Tcr)
        WHERE db.id IN ["VDJdb", "IEDB"]
        RETURN count(DISTINCT tcr)
    """,
    r"...with only TCR$\beta$": """
        MATCH (db:Database)--(:Study)--(:Annotation)--(tcr:Tcr)--(trb:Trb)
        WHERE db.id IN ["VDJdb", "IEDB"] AND NOT (tcr)--(:Tra)
        MATCH (trb)--(jb:JBeta)
        MATCH (trb)--(vb:VBeta)
        MATCH (trb)--(cb:Cdr3Beta)
        RETURN count(DISTINCT trb)
    """,
    "...with inferred partner": """
        MATCH (db:Database)--(:Study)--(:Annotation)--(tcr:Tcr)--(trb:Trb)
        WHERE db.id IN ["VDJdb", "IEDB"] AND NOT (tcr)--(:Tra)
        MATCH (trb)--(jb:JBeta)
        MATCH (trb)--(vb:VBeta)
        MATCH (trb)--(cb:Cdr3Beta)
        WITH DISTINCT trb, jb, vb, cb
        MATCH (trb)--(tcr:Tcr)--(tra:Tra)
        MATCH (tra)--(ja:JAlpha)
        MATCH (tra)--(va:VAlpha)
        MATCH (tra)--(ca:Cdr3Alpha)
        MATCH (tcr)--(c:Clone)
        WHERE (c)-[:SAMPLED_FROM]-(:Repertoire)-[:IS_IN*0..2]-(:Repertoire)-[:IN_STUDY]-(:Study {id: "TannoEtAl"}) OR
        (c)-[:SAMPLED_FROM]-(:Repertoire)-[:IS_IN*0..2]-(:Repertoire)-[:IN_STUDY]-(:Study)-[:IS_IN]-(:Database {id: "OTS"})
        RETURN count(DISTINCT trb)
    """,
    r"TCR$\alpha \beta$ w/o known pMHC": """
        MATCH (:Cdr3Alpha)--(tra:Tra)--(tcr:Tcr)--(trb:Trb)--(:Cdr3Beta)
        MATCH (trb)--(:JBeta)
        MATCH (trb)--(:VBeta)
        MATCH (tra)--(:JAlpha)
        MATCH (tra)--(:VAlpha)
        MATCH (tcr)--(c:Clone)
        WHERE (c)-[:SAMPLED_FROM]-(:Repertoire)-[:IS_IN*0..2]-(:Repertoire)-[:IN_STUDY]-(:Study {id: "TannoEtAl"}) OR
        (c)-[:SAMPLED_FROM]-(:Repertoire)-[:IS_IN*0..2]-(:Repertoire)-[:IN_STUDY]-(:Study)-[:IS_IN]-(:Database {id: "OTS"})
        RETURN count(DISTINCT tcr)
    """,
}

results = {}
with driver.session() as session:
    for name, query in queries.items():
        result = session.run(query)
        count = result.single()[0]
        results[name] = count
        print(f"{name}: {count:,}")

driver.close()

fig, ax = plt.subplots(figsize=(5, 5))

labels = list(results.keys())
counts = list(results.values())
colors = sns.color_palette("crest", n_colors=len(labels))

bars = ax.bar(range(len(labels)), counts, color=colors)
ax.set_yscale("log")
ax.set_ylim(bottom=1, top=1e7)
ax.set_ylabel("Count")
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=45, ha="right")

for i, (bar, count) in enumerate(zip(bars, counts)):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0,
        height,
        f"{count:,}",
        ha="center",
        va="bottom",
    )

fig.tight_layout()
fig.savefig("ann_trb_partner_inference.svg")
fig.savefig("ann_trb_partner_inference.pdf")
fig.show()

print("\n" + "=" * 50)
print("Analysis complete!")
print("=" * 50)

