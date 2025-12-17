# back/run-tests.sh
#!/bin/bash
echo "Running unit tests..."
pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed!"
    exit 1
fi