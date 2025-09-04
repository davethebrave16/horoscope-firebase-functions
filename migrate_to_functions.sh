#!/bin/bash

# Migration script to move from root-level to functions/ directory structure

echo "Starting migration to Firebase Functions structure..."

# Backup original main.py
echo "Creating backup of original main.py..."
cp main.py main.py.backup

# Create .env.example if it doesn't exist
if [ ! -f .env.example ]; then
    echo "Creating .env.example file..."
    cat > .env.example << EOF
# API Key for authentication
API_KEY=your-api-key-here
EOF
fi

# Update .gitignore to include functions/venv
if ! grep -q "functions/venv" .gitignore 2>/dev/null; then
    echo "Updating .gitignore..."
    echo "functions/venv/" >> .gitignore
fi

echo "Migration completed!"
echo ""
echo "Next steps:"
echo "1. Set your API_KEY in .env file: echo 'API_KEY=your-key' > .env"
echo "2. Test locally: cd functions && firebase emulators:start --only functions"
echo "3. Deploy: firebase deploy --only functions"
echo ""
echo "Original main.py has been backed up as main.py.backup"
