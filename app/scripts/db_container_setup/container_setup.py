"""This script is used to wait for a PostgreSQL database to become available and then create required extensions and migrate the database schema.
"""

#!/usr/bin/env python3


import socket
import subprocess
import time
import sys
from dotenv import load_dotenv


load_dotenv()


def _migrate_database():
    """Run database schema migration using Alembic."""
    subprocess.run(["alembic", "upgrade", "head"], check=True)


def wait_for_db(db_host_arg, db_port_arg, timeout=30):
    """Wait for the PostgreSQL database to become available."""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((db_host_arg, db_port_arg), timeout=5):
                _migrate_database()
                return True
        except (socket.timeout, ConnectionRefusedError):
            pass

        if time.time() - start_time >= timeout:
            return False

        time.sleep(1)


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])
    if wait_for_db(host, port):
        print("Database is ready to receive connections!")
        subprocess.run(["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", str(api_port), "--reload"], check=True)
        sys.exit(0)
    else:
        sys.exit(1)
