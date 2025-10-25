# 🏦 Payment Wallet System 

A digital wallet system built using **Python, Django, and Django REST Framework**, implementing real financial transaction principles such as **double-entry ledger accounting**, **atomic balance updates**, **idempotent transfers**, and **row-level locking** to prevent race conditions.

---

## 🚀 Features

| Feature | Status | Description |
|--------|--------|-------------|
| Add Money | ✅ | Users can top up their wallet balance |
| Transfer Money | ✅ | Safe wallet-to-wallet transfers |
| Ledger System | ✅ | Double-entry ledger (Debit + Credit) maintains accuracy |
| Race Condition Safety | ✅ | `transaction.atomic()` + `select_for_update()` to prevent double-spend |
| Idempotent Transfers | ✅ | Duplicate transfer requests are ignored via `reference_id` |
| REST APIs | ✅ | `/api/wallet/` and `/api/transactions/` return JSON data |
| User Auth System | ✅ | Signup + Login + Django session auth |
| UI Pages | ✅ | Dashboard, Add Money, Transfer, Transaction History |

---

## 🧠 Architecture Overview

               ┌──────────────────────────────┐
               │          Web Browser          │
               │  (User interacts via UI)      │
               └──────────────┬───────────────┘
                              │ HTTP Requests
                              ▼
                      ┌───────────────────┐
                      │   Django Views     │
                      │ (wallet/views.py)  │
                      └─────────┬─────────┘
                                │ Business Logic
                                ▼
             ┌────────────────────────────────────────┐
             │   transaction.atomic() + select_for_update()  │
             │   Ensures atomicity + prevents race conditions │
             └───────────────────┬───────────────────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────┐
                  │       Database           │
                  │ (SQLite / PostgreSQL)    │
                  └───────────┬──────────────┘
                              │
         ┌────────────────────┴─────────────────────┐
         │                                          │
┌────────────────────┐                  ┌─────────────────────┐
│      Wallet         │                  │    Transaction      │
│ (One per user)      │                  │ (Double-entry ledger)│
└────────────────────┘                  └─────────────────────┘

```UI sends requests → Django applies business rules → Atomic + locked update → Wallet + Transaction tables remain consistent.```



### Why Double-Entry Ledger?
A transfer creates **two** entries:
- **Debit** from sender
- **Credit** to receiver

This ensures:
✅ Financial correctness  
✅ Full audit history  
✅ Balance = Sum(credits) - Sum(debits)

---

## 🗄 Database Models

| Model | Purpose |
|------|---------|
| **Wallet** | One per user. Stores current balance. |
| **Transaction** | Each money movement logged as debit or credit. |

---

## 🔐 Consistency & Safety Mechanisms

| Mechanism | What it Solves |
|----------|----------------|
| `transaction.atomic()` | Ensures all-or-nothing database updates. |
| `select_for_update()` | Prevents two transfers from modifying same wallet at once (race condition safety). |
| `reference_id` idempotency key | Prevents duplicate transfers on refresh/retry. |

These are the **same principles used in Paytm, PhonePe, Razorpay, UPI wallets**.

---

## 🌐 REST API Endpoints (JSON Responses)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/wallet/` | Returns current user's wallet balance. |
| GET | `/api/transactions/` | Returns user's transaction ledger history. |

### Testing with Postman
1. Login in browser at `/accounts/login/`
2. Copy `sessionid` cookie
3. Add in Postman request headers:   Cookie: sessionid=YOUR_VALUE_HERE



---

## 🏁 Run Project Locally

```bash
git clone <your-repo-url>
cd payment_wallet
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open in browser:  ```http://127.0.0.1:8000/```


## 📦 Dependencies
- All required dependencies are listed in `requirements.txt`.
- To generate (if needed): ```pip freeze > requirements.txt```

---

## 📌 Project Screens (UI Features)

| Screen | Purpose |
|--------|---------|
| **Dashboard** | View wallet balance + transaction history |
| **Add Money** | Increase wallet balance |
| **Transfer Money** | Send money to another user |
| **Login & Signup** | Secure access to wallet |

---

### 🎤 Interview Summary 

The wallet uses a double-entry ledger, so every transfer generates both a debit and a credit entry, ensuring auditability and correctness.
Transfers run inside a transaction.atomic() block with select_for_update() to lock wallet rows and prevent race conditions and double-spending.
An idempotency key (reference_id) prevents duplicate transfers on refresh or network retries.
Wallet balance and transaction history are exposed through REST APIs for easy frontend/mobile integration.



### ✨ Future Enhancements

1. JWT Authentication for API access
2. Razorpay / UPI integration for real payments
3. Admin reporting dashboard & analytics

### ⭐ Author

Designed to demonstrate backend system design, ledger integrity, consistency handling, and secure financial transactions.

