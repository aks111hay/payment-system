from flask import Flask, render_template, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import razorpay
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red, black,white
import io
import os

# Custom Ticket Size
TICKET_WIDTH = 800  # Small width
TICKET_HEIGHT = 800  # Small height
TICKET_SIZE = (TICKET_WIDTH, TICKET_HEIGHT)

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Razorpay API Keys
RAZORPAY_KEY_ID = ""
RAZORPAY_KEY_SECRET = ""
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Define Ticket Model
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    ticket_type = db.Column(db.String(50), nullable=False)
    ticket_id = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Ticket {self.ticket_id}>"

# Create Database
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("razorpay_ticket_form.html")

@app.route("/create-order", methods=["POST"])
def create_order():
    try:
        data = request.json
        amount = int(data.get("amount", 0))  # Amount in paise

        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400

        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        }

        order = razorpay_client.order.create(order_data)
        return jsonify(order)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-ticket", methods=["POST"])
def generate_ticket():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        contact = data.get("contact")
        ticket_type = data.get("ticket")
        transactionId = data.get("transactionId")

        if not all([name, email, contact, ticket_type]):
            return jsonify({"error": "Missing required fields"}), 400

        # Generate Unique Ticket ID
        last_ticket = Ticket.query.filter_by(ticket_type=ticket_type).order_by(Ticket.id.desc()).first()
        ticket_number = last_ticket.id + 1 if last_ticket else 1
        # ticket_id = f"tedxnielit{ticket_type.lower()}{ticket_number}"
        ticket_id = transactionId

        # Save Ticket to Database
        new_ticket = Ticket(name=name, email=email, contact=contact, ticket_type=ticket_type, ticket_id=ticket_id)
        db.session.add(new_ticket)
        db.session.commit()
        id = Ticket.query.filter_by(ticket_id = ticket_id).first()

        # Generate QR Code
        qr_data = f"Ticket ID: {ticket_id}\nID: {id.id}"
        qr = qrcode.make(qr_data)
        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        
        # create pdf
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=TICKET_SIZE)
        pdf.setTitle("TEDXNielit Aurangabad Ticket")

         # Background Color (Optional)
        pdf.setFillColor(red)
        pdf.rect(0, 0, TICKET_WIDTH, TICKET_HEIGHT, fill=True, stroke=False)
        
        pdf.setFillColor(white)
        
        
        # Load TEDx Header Image (Full Width)
        header_path = "static/footer.png"  # Make sure the file exists
        if os.path.exists(header_path):
            pdf.drawInlineImage(header_path, 0, TICKET_HEIGHT -180, width=TICKET_WIDTH, height=180)  # Top Full Width
        # Event Details (White Text for Consistency)
        pdf.setFont("Helvetica", 20)
        pdf.drawString(50, 550, f"Name: {name}")
        pdf.drawString(50, 520, f"Email: {email}")
        pdf.drawString(50, 490, f"Contact: {contact}")
        pdf.setFillColor(black)
        pdf.setFont("Helvetica-Bold",20)
        pdf.drawString(50, 460, f"Ticket Type: {ticket_type.capitalize()}")
        pdf.drawString(50, 430, f"Ticket ID: {ticket_id}")
        pdf.setFillColor(white)
        # Event Venue & Date Section (White on Red)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(50, 350, "Event Date: 20th March 2025")
        pdf.drawString(50, 320, "Venue: NIELIT Auditorium, Aurangabad")

        # Footer Red Background
        pdf.rect(0, 50, TICKET_WIDTH, 100, fill=1)  # Footer background
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(300, 90, "TEDx Official Ticket")

        # Draw QR Code (Aligned to the Right, Centered)
        qr_image_path = "qr_code.png"
        with open(qr_image_path, "wb") as f:
            f.write(qr_buffer.getvalue())

        pdf.drawInlineImage(qr_image_path, 500,440, width=150, height=150)  # Centered QR


        # Load Footer Image (Full Width)
        footer_path = "static/footer.png"  # Make sure the file exists
        if os.path.exists(footer_path):
            pdf.drawInlineImage(footer_path, 0, 0, width=TICKET_WIDTH, height=160)  # Bottom Full Width

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        os.remove(qr_image_path)  # Clean up QR code image

        return send_file(buffer, as_attachment=True, download_name="TEDx_Ticket.pdf", mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
