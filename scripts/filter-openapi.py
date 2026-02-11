#!/usr/bin/env python3
"""
Скрипт для фильтрации OpenAPI спецификации, исключая admin эндпоинты.
"""
import json
import sys
from collections import defaultdict
from urllib.request import urlopen


SCHEMA_REF_PREFIX = "#/components/schemas/"
SECURITY_REF_PREFIX = "#/components/securitySchemes/"


def _walk_refs(node, prefix: str) -> set[str]:
    refs: set[str] = set()

    def _walk(value):
        if isinstance(value, dict):
            ref = value.get("$ref")
            if isinstance(ref, str) and ref.startswith(prefix):
                refs.add(ref[len(prefix):])
            for inner in value.values():
                _walk(inner)
        elif isinstance(value, list):
            for inner in value:
                _walk(inner)

    _walk(node)
    return refs


def _normalize_operation_tags(tags: list[str]) -> list[str]:
    """Нормализует теги операций для стабильной группировки в Mintlify."""
    normalized: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        if not isinstance(tag, str):
            continue
        key = tag.strip().lower()
        if not key:
            continue
        if key not in seen:
            normalized.append(key)
            seen.add(key)

    return normalized


def _build_tags_metadata(tag_usage: dict[str, int]) -> list[dict]:
    descriptions = {
        "insight": "Core insight endpoints: records, transcripts, generation, and chat.",
        "insight_public": "Public insight endpoints for shared/public access.",
        "projects": "Project management endpoints.",
        "project_reports": "Project report generation and management endpoints.",
        "project_reports_public": "Public project report endpoints.",
        "prompts": "Custom prompts management endpoints.",
        "presets": "Presets and templates endpoints.",
        "agent": "AI agent threads and chat endpoints.",
        "interviews": "AI interviewer room and session endpoints.",
        "webhooks": "Incoming webhook endpoints.",
    }
    ordered_names = [
        "insight",
        "insight_public",
        "projects",
        "project_reports",
        "project_reports_public",
        "prompts",
        "presets",
        "agent",
        "interviews",
        "webhooks",
    ]

    tags: list[dict] = []
    for name in ordered_names:
        if name in tag_usage:
            tags.append(
                {
                    "name": name,
                    "description": descriptions.get(name, f"{name} endpoints."),
                    "x-displayName": name.replace("_", " ").title(),
                }
            )

    for name in sorted(tag_usage):
        if name in {t["name"] for t in tags}:
            continue
        tags.append(
            {
                "name": name,
                "description": f"{name} endpoints.",
                "x-displayName": name.replace("_", " ").title(),
            }
        )
    return tags


def _apply_agent_english_overrides(data: dict) -> None:
    """Переопределяет русские описания agent-эндпоинтов и связанных схем на английский."""
    operation_descriptions = {
        "chat_agent_chat_post": (
            "Send a message to the AI agent and receive a streaming response.\n\n"
            "Request body:\n"
            "- thread_id: Agent thread ID\n"
            "- message: User message text\n\n"
            "Returns:\n"
            "- Streaming response chunks"
        ),
        "get_threads_agent_threads_get": (
            "Get all agent threads for the current user.\n\n"
            "Returns:\n"
            "- List of user threads"
        ),
        "create_thread_agent_threads_post": (
            "Create a new agent thread.\n\n"
            "Request body:\n"
            "- name: Optional thread name\n\n"
            "Returns:\n"
            "- Created thread object"
        ),
        "update_thread_agent_threads__thread_id__patch": (
            "Update an existing agent thread.\n\n"
            "Path params:\n"
            "- thread_id: Thread ID\n\n"
            "Request body:\n"
            "- name: New thread name\n\n"
            "Returns:\n"
            "- Updated thread object"
        ),
        "delete_thread_agent_threads__thread_id__delete": (
            "Soft-delete an agent thread.\n\n"
            "Path params:\n"
            "- thread_id: Thread ID"
        ),
        "get_thread_agent_threads__thread_id__get": (
            "Get an agent thread by ID.\n\n"
            "Path params:\n"
            "- thread_id: Thread ID\n\n"
            "Returns:\n"
            "- Thread object"
        ),
        "get_history_agent_threads__thread_id__history_get": (
            "Get message history for an agent thread.\n\n"
            "Path params:\n"
            "- thread_id: Thread ID\n\n"
            "Returns:\n"
            "- Ordered list of thread messages"
        ),
        "cancel_chat_agent_chat_cancel_post": (
            "Cancel an in-progress chat request.\n\n"
            "Request body:\n"
            "- thread_id: Thread ID\n\n"
            "Returns:\n"
            "- Cancellation status"
        ),
    }

    schema_descriptions = {
        "AgentMessageDTO": "Data transfer object for an agent message.",
        "AgentThreadDTO": "Data transfer object for an agent thread.",
        "CancelChatRequest": "Request model for canceling an in-progress chat.",
        "CreateThreadRequest": "Request model for creating an agent thread.",
        "Services__AgentService__models__ChatRequest": "Request model for sending a chat message.",
        "UpdateThreadRequest": "Request model for updating an agent thread.",
    }

    for path_item in data.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            if operation_id in operation_descriptions:
                operation["description"] = operation_descriptions[operation_id]

    schemas = data.get("components", {}).get("schemas", {})
    for schema_name, description in schema_descriptions.items():
        schema = schemas.get(schema_name)
        if isinstance(schema, dict):
            schema["description"] = description


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

    # Mintlify ожидает servers для корректного рендера endpoint-страниц.
    if not data.get("servers"):
        data["servers"] = [{"url": "https://app.aseed.ai/custdev"}]
    
    # Фильтруем paths, исключая эндпоинты с тегом 'admin'
    filtered_paths = {}
    removed_count = 0
    tag_usage: defaultdict[str, int] = defaultdict(int)

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
            normalized_tags = _normalize_operation_tags(tags)
            if 'admin' in normalized_tags:
                has_admin = True
                removed_count += 1
                print(f"  Удален: {method.upper()} {path} (тег: {tags})", file=sys.stderr)
            else:
                if normalized_tags:
                    operation['tags'] = normalized_tags
                    for tag in normalized_tags:
                        tag_usage[tag] += 1
                filtered_operations[method] = operation
        
        # Добавляем path только если в нем нет admin операций
        if not has_admin:
            filtered_paths[path] = filtered_operations
    
    data['paths'] = filtered_paths

    # Добавляем явные метаданные тегов для стабильного рендера групп.
    data['tags'] = _build_tags_metadata(tag_usage)

    # Нормализуем описания agent-раздела на английский.
    _apply_agent_english_overrides(data)

    # Prune components.schemas до реально используемых (включая транзитивные ссылки).
    components = data.get('components', {})
    schemas = components.get('schemas', {})
    referenced_schemas = _walk_refs(filtered_paths, SCHEMA_REF_PREFIX)
    queue = list(referenced_schemas)
    while queue:
        schema_name = queue.pop()
        schema = schemas.get(schema_name)
        if not isinstance(schema, dict):
            continue
        for ref in _walk_refs(schema, SCHEMA_REF_PREFIX):
            if ref not in referenced_schemas:
                referenced_schemas.add(ref)
                queue.append(ref)

    if schemas:
        components['schemas'] = {
            name: schema
            for name, schema in schemas.items()
            if name in referenced_schemas
        }

    # Prune components.securitySchemes до реально используемых.
    referenced_security = _walk_refs(filtered_paths, SECURITY_REF_PREFIX)
    for path_item in filtered_paths.values():
        if not isinstance(path_item, dict):
            continue
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            for sec_obj in operation.get('security', []):
                if isinstance(sec_obj, dict):
                    referenced_security.update(sec_obj.keys())
    for sec_obj in data.get('security', []):
        if isinstance(sec_obj, dict):
            referenced_security.update(sec_obj.keys())

    security_schemes = components.get('securitySchemes', {})
    if security_schemes:
        components['securitySchemes'] = {
            name: scheme
            for name, scheme in security_schemes.items()
            if name in referenced_security
        }

    data['components'] = components

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
