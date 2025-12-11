#!/usr/bin/env python3
"""
Скрипт для фильтрации OpenAPI спецификации, исключая admin эндпоинты.
"""
import json
import sys
from urllib.request import urlopen


def filter_admin_endpoints(openapi_url: str) -> dict:
    """
    Загружает OpenAPI спецификацию и удаляет все эндпоинты с тегом 'admin'.
    
    Args:
        openapi_url: URL OpenAPI спецификации
        
    Returns:
        Отфильтрованная OpenAPI спецификация
    """
    # Загружаем OpenAPI спецификацию
    with urlopen(openapi_url) as response:
        data = json.load(response)
    
    # Фильтруем paths, исключая эндпоинты с тегом 'admin'
    filtered_paths = {}
    removed_count = 0
    
    for path, path_item in data.get('paths', {}).items():
        # Исключаем эндпоинты, которые содержат '/admin' в пути
        if '/admin' in path.lower():
            # Подсчитываем количество операций в этом path
            operations_count = sum(1 for op in path_item.values() if isinstance(op, dict))
            removed_count += operations_count
            print(f"  Удален: {path} ({operations_count} операций) - содержит '/admin' в пути", file=sys.stderr)
            continue
        
        # Проверяем все операции в path (get, post, put, delete, patch и т.д.)
        filtered_operations = {}
        has_admin = False
        
        for method, operation in path_item.items():
            if not isinstance(operation, dict):
                # Это не операция (например, parameters, servers)
                filtered_operations[method] = operation
                continue
                
            # Проверяем теги операции
            tags = operation.get('tags', [])
            if 'admin' in [tag.lower() for tag in tags]:
                has_admin = True
                removed_count += 1
                print(f"  Удален: {method.upper()} {path} (тег: {tags})", file=sys.stderr)
            else:
                filtered_operations[method] = operation
        
        # Добавляем path только если в нем нет admin операций
        if not has_admin:
            filtered_paths[path] = filtered_operations
    
    data['paths'] = filtered_paths
    
    print(f"Всего эндпоинтов: {len(data.get('paths', {})) + removed_count}", file=sys.stderr)
    print(f"Оставлено эндпоинтов: {len(filtered_paths)}", file=sys.stderr)
    print(f"Удалено admin эндпоинтов: {removed_count}", file=sys.stderr)
    
    return data


def main():
    """Основная функция."""
    if len(sys.argv) < 2:
        print("Использование: python filter-openapi.py <openapi_url> [output_file]", file=sys.stderr)
        print("Пример: python filter-openapi.py https://app.aseed.ai/custdev/openapi.json api-reference/openapi-filtered.json", file=sys.stderr)
        sys.exit(1)
    
    openapi_url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        filtered_data = filter_admin_endpoints(openapi_url)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f, indent=2, ensure_ascii=False)
            print(f"\nОтфильтрованная спецификация сохранена в: {output_file}", file=sys.stderr)
        else:
            # Выводим в stdout
            print(json.dumps(filtered_data, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
