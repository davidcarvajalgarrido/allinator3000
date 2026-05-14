import os
from dotenv import load_dotenv
import pg8000
from google.cloud.sql.connector import Connector

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

INSTANCE_CONNECTION_NAME = f"{os.environ['IDPROJECT']}:{os.environ['REGION']}:{os.environ['BDINSTANCE']}"
DB_NAME = os.environ["BDNAME"]
DB_USER = os.environ["BDUSER"]
DB_PASS = os.environ["BDPASS"]

def get_cloud_types() -> list[dict]:
    connector = Connector()

    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )

    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, description, altitude_min_m, altitude_max_m, created_at FROM cloud_types"
    )
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    connector.close()

    return [dict(zip(columns, row)) for row in rows]


if __name__ == "__main__":
    cloud_types = get_cloud_types()
    for ct in cloud_types:
        print(ct)
