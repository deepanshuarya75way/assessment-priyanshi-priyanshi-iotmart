# 🛒 IoTMart - IoT E-Commerce & Hardware Platform

[![Live Demo](https://img.shields.io/badge/Live--Demo-Visit%20Site-00C853?style=for-the-badge&logo=render)](https://iotmart-sdee.onrender.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?logo=react)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-8.0-646CFF?logo=vite)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.0-38BDF8?logo=tailwindcss)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?logo=python)](https://fastapi.tiangolo.com/)

🌐 **Live Web Application:** [https://iotmart-sdee.onrender.com/](https://iotmart-sdee.onrender.com/)  
⚡ **Live Backend API:** [https://iotmart-backend-kbp2.onrender.com](https://iotmart-backend-kbp2.onrender.com)

A modern, full-featured E-Commerce web application dedicated to Internet of Things (IoT) hardware, microcontrollers, sensors, and developer kits. Built with high performance, dynamic filtering, responsive UI, payment gateway integrations, and an intuitive admin dashboard.

---

## ✨ Features

- ⚡ **Lightning Fast UI**: Built with React 19 & Vite for near-instant rendering and Hot Module Replacement (HMR).
- 📦 **IoT Catalog & Hardware Categories**: Browse sensors, microcontrollers (ESP32, Arduino, Raspberry Pi), actuators, and developer kits with dynamic search & multi-tag filtering.
- 🛒 **Interactive Shopping Cart & Order Flow**: Add/remove items, apply promo codes, and manage order summaries dynamically.
- 💳 **Payment & Checkout Integration**: Native integration support for Cashfree payment gateway & digital payment workflows.
- 🔐 **Authentication & Security**: Secure JWT authentication, user registration, Google OAuth support, and role-based access control (User vs. Admin).
- 📜 **Invoice & Review Generation**: PDF invoice downloading (jspdf) and verified buyer review system.
- 📊 **Admin Dashboard & Analytics**: Interactive charts (Recharts) and inventory control for managing products, orders, and users.

---

## 🛠️ Tech Stack

- **Frontend**: React 19, React Router DOM v7, Tailwind CSS v4, Framer Motion, Lucide Icons, Recharts, Monaco Editor
- **Backend / API**: Python FastAPI, MongoDB / PyMongo, JWT Auth, Brevo / Twilio Integration
- **Build Tooling**: Vite 8, ESLint, PostCSS, PWA Plugin

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Node.js (v18+ recommended) and npm installed.

### 1. Clone the repository
```bash
git clone https://github.com/priyanshi1311/iotmart.git
cd iotmart
```

### 2. Install dependencies
```bash
npm install
```

### 3. Start the development server
```bash
npm run dev
```

The application will start at `http://localhost:5173`.

---

## 📂 Project Structure

```
iotmart/
├── src/
│   ├── components/      # Reusable UI components (Navbar, Footer, Modals, Cards)
│   ├── pages/           # Application views (Home, Shop, ProductDetails, Cart, Admin)
│   ├── context/         # React context states (Auth, Cart, Theme)
│   ├── services/        # API clients & Axios interceptors
│   └── utils/           # Utility functions & helpers
├── backend/             # Python FastAPI backend service & seed scripts
├── public/              # Static assets & icons
└── vite.config.js       # Vite configuration
```

---

## 👩‍💻 Author

Developed & Maintained by **[Priyanshi Bhati](https://github.com/priyanshi1311)**.
