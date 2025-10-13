#!/bin/bash
# Run tests with coverage

echo "🧪 Running tests..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
pytest \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    -v \
    "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
    echo "📊 Coverage report generated:"
    echo "   - Terminal: See above"
    echo "   - HTML: htmlcov/index.html"
    echo "   - XML: coverage.xml"
else
    echo ""
    echo "❌ Some tests failed"
fi

exit $exit_code
