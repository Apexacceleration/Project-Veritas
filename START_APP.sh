#!/bin/bash
# Project Veritas - Start Script

echo "🚀 Starting Project Veritas..."
echo ""

cd "/Users/apexacceleration/My Drive (tyler@apexacceleration.com) (1)/Software Projects/Project Veritas"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "   Create one with: echo 'OPENAI_API_KEY=your-key' > .env"
    echo ""
fi

# Start Streamlit
echo "📍 Opening http://localhost:8501"
echo "🛑 Press Ctrl+C to stop"
echo ""

streamlit run app.py
