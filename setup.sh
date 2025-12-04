#!/bin/bash

# Setup script for Thinking Engine

echo "🚀 Setting up AI Content Thinking Engine..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
else
    echo "✓ .env file already exists"
fi

# Create output directory
mkdir -p output

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Add curated articles to data/week-YYYY-MM-DD/"
echo "3. Run: python -m src.thinking_engine.cli generate-all"
echo ""

