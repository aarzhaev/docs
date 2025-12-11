#!/bin/bash
# Скрипт для обновления отфильтрованной OpenAPI спецификации

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
OPENAPI_URL="https://app.aseed.ai/custdev/openapi.json"
OUTPUT_FILE="$DOCS_DIR/api-reference/openapi-filtered.json"

echo "🔄 Обновление отфильтрованной OpenAPI спецификации..."
echo "   URL: $OPENAPI_URL"
echo "   Output: $OUTPUT_FILE"

python3 "$SCRIPT_DIR/filter-openapi.py" "$OPENAPI_URL" "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Отфильтрованная OpenAPI спецификация успешно обновлена"
else
    echo "❌ Ошибка при обновлении OpenAPI спецификации"
    exit 1
fi
