from typing import Dict, Any, List

def validate_branch_name(branch_name: str) -> Dict[str, Any]:
    """
    Проверка имени ветки.
    
    Args:
        branch_name: Имя ветки для проверки
        
    Returns:
        Словарь с результатом проверки
    """
    # Проверяем, является ли имя ветки допустимым для Git
    # Это упрощенная проверка, реальная реализация была бы более комплексной
    
    invalid_chars = ['~', '^', ':', '\\', '*', '?', '[', ' ']
    errors = []
    
    if any(char in branch_name for char in invalid_chars):
        errors.append(f"Branch name contains invalid characters: {', '.join(invalid_chars)}")
    
    if branch_name.startswith('.') or branch_name.endswith('.'):
        errors.append("Branch name cannot start or end with a dot")
    
    if branch_name.endswith('.lock'):
        errors.append("Branch name cannot end with '.lock'")
        
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def validate_release_name(release_name: str) -> Dict[str, Any]:
    """
    Проверка имени релиза.
    
    Args:
        release_name: Имя релиза для проверки
        
    Returns:
        Словарь с результатом проверки
    """
    errors = []
    
    if len(release_name) < 2:
        errors.append("Release name is too short (minimum 2 characters)")
    
    if len(release_name) > 50:
        errors.append("Release name is too long (maximum 50 characters)")
        
    return {
        "valid": len(errors) == 0,
        "errors": errors
    } 