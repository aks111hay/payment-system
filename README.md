# 🚀 Razorpay Payment Integration for Event Management

## 📌 Overview
This repository provides an **Event Management System** with integrated **Razorpay payment gateway**, allowing users to book event tickets and make secure online payments.

## 🎯 Features  
✅ Razorpay payment gateway integration  
✅ Secure online transactions  
✅ Payment success and failure handling  
✅ Responsive UI for a seamless user experience  

## 🛠 Tech Stack
- **Frontend**: HTML, CSS, JavaScript (or React if applicable)  
- **Backend**: Python, Flask  
- **Database**: MongoDB / MySQL  
- **Payment Gateway**: Razorpay API  

## 📦 Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/aks111hay/payment-system.git
   cd razorpay-event-management
   ```
2. **Install dependencies:**
   ```bash
   pip install flask
   pip imstall flask sqlalchemy
   pip install razorpay
   pip install reportlab
   pip install qrcode
   ```
3. **Set up environment variables:**
   Create a `.env` file and add:
   ```env
   RAZORPAY_KEY_ID=your_razorpay_key
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   FLASK_APP=app.py
   FLASK_ENV=development
   ```
4. **Start the Flask server:**
   ```bash
   python app.py
   ```

## 🎟 How It Works
1. Users select an event and proceed to payment.  
2. Payment is processed via **Razorpay API**.  
3. Upon successful payment, a confirmation is displayed.  
4. Payment failure is also handled with proper alerts.  


## 📜 License
This project is **open-source** and available under the **MIT License**.

## 🤝 Contributing
Contributions are welcome! Feel free to fork, open an issue, or submit a pull request.

