from flask import Flask, jsonify

import lakebase
app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"status": "app is running"})


@app.route("/tickets")
def get_tickets():
    rows = lakebase.run_query(
        """
        SELECT
            ticket_id,
            title,
            status,
            created_by,
            created_at
        FROM tickets
        ORDER BY created_at DESC
        """
    )

    return jsonify(rows)
