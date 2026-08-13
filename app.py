from flask import Flask, jsonify, request, render_template
import lakebase

app = Flask(__name__)

@app.route("/")
def home():

    stats = lakebase.run_query(
        """
        SELECT
            COUNT(*) AS total_tickets,
            SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) AS open_tickets,
            SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) AS resolved_tickets
        FROM tickets
        """
    )[0]

    return render_template(
        "index.html",
        stats=stats
    )


@app.route("/tickets")
def get_tickets():

    status = request.args.get("status")

    if status:

        rows = lakebase.run_query(
            """
            SELECT
                ticket_id,
                title,
               	status,
                priority,
                created_by,
                created_at
            FROM tickets
            WHERE status = %s
            ORDER BY created_at DESC
            """,
            (status,),
        )

    else:

        rows = lakebase.run_query(
            """
            SELECT
                ticket_id,
                title,
                status,
                priority,
                created_by,
                created_at
            FROM tickets
            ORDER BY created_at DESC
            """
        )

    return render_template(
        "tickets.html",
        tickets=rows,
    )

@app.route("/tickets/<int:ticket_id>/messages")
def get_messages(ticket_id):

    rows = lakebase.run_query(
        """
        SELECT
            message_id,
            message_text,
            author,
            created_at
        FROM ticket_messages
        WHERE ticket_id = %s
        ORDER BY created_at
        """,
        (ticket_id,),
    )

    return render_template(
        "messages.html",
        messages=rows
    )


@app.route("/tickets", methods=["POST"])
def create_ticket():

    data = request.get_json()

    lakebase.run_write(
        """
        INSERT INTO tickets
        (title, status, created_by, created_at)
        VALUES (%s, %s, %s, NOW())
        """,
        (
            data["title"],
            "open",
            data["created_by"],
        ),
    )

    return jsonify({"message": "Ticket created"})


@app.route("/tickets/<int:ticket_id>/messages", methods=["POST"])
def add_message(ticket_id):

    data = request.get_json()

    lakebase.run_write(
        """
        INSERT INTO ticket_messages
        (ticket_id, message_text, author, created_at)
        VALUES (%s, %s, %s, NOW())
        """,
        (
            ticket_id,
            data["message_text"],
            data["author"],
        ),
    )

    return jsonify({"message": "Message added"})


@app.route("/tickets/<int:ticket_id>/status", methods=["PATCH"])
def update_status(ticket_id):

    data = request.get_json()

    lakebase.run_write(
        """
        UPDATE tickets
        SET status = %s
        WHERE ticket_id = %s
        """,
        (
            data["status"],
            ticket_id,
        ),
    )

    return jsonify({"message": "Status updated"})