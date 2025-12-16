#!/bin/bash

# ESP32-CAM Davomat Tizimi - Quick Start Script

echo "🚀 ESP32-CAM Davomat Tizimi - Quick Start"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 topilmadi. Iltimos Python 3.8+ o'rnating."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL topilmadi. Iltimos PostgreSQL o'rnating."
    echo "   Ubuntu/Debian: sudo apt install postgresql"
    echo "   macOS: brew install postgresql"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js topilmadi. Iltimos Node.js 18+ o'rnating."
    exit 1
fi

echo ""
echo "📦 1. Backend sozlash..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "   Virtual environment yaratilmoqda..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "   Dependencies o'rnatilmoqda..."
pip install -q -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "   .env fayl yaratilmoqda..."
    cp .env.example .env
    echo "   ⚠️  .env faylni tahrirlang va to'ldiring!"
fi

cd ..

echo ""
echo "📦 2. Frontend sozlash..."
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "   Dependencies o'rnatilmoqda..."
    npm install
fi

# Create .env.local if not exists
if [ ! -f ".env.local" ]; then
    echo "   .env.local yaratilmoqda..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi

cd ..

echo ""
echo "✅ Sozlash tugadi!"
echo ""
echo "📋 Keyingi qadamlar:"
echo "   1. PostgreSQL database yarating:"
echo "      psql -U postgres -c 'CREATE DATABASE attendance_db;'"
echo "      psql -U postgres -d attendance_db -f backend/database/schema.sql"
echo ""
echo "   2. backend/.env faylni to'ldiring"
echo ""
echo "   3. Backend ishga tushiring:"
echo "      cd backend && source venv/bin/activate && python main.py"
echo ""
echo "   4. Frontend ishga tushiring (yangi terminal):"
echo "      cd frontend && npm run dev"
echo ""
echo "   5. Brauzerda oching: http://localhost:3000"
echo ""
