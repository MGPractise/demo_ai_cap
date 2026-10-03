import traceback
from neo4j import GraphDatabase

# URI = "neo4j+s://ed5b5964.databases.neo4j.io"
# USERNAME = "ed5b5964"
# PASSWORD = "u48J0huFmWC5Ri2oZY76qbPbKQ0A8qkLofGUn1WT2Ws"

URI = "neo4j+s://1e770572.databases.neo4j.io"
USERNAME = "1e770572"
PASSWORD = "cH84hFjJDDS0dRF8YezS6X_D8ZIeDGE2kAqTN6X0yJI"



driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD),
)

try:
    driver.verify_connectivity()
    print("CONNECTED")

except Exception:
    traceback.print_exc()

finally:
    driver.close()
