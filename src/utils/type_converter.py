"""
Конвертация типов данных (numpy, pandas -> стандартные Python типы)
"""
import numpy as np
import pandas as pd
from typing import Any


def convert_numpy_types(obj: Any) -> Any:
    """
    Рекурсивно преобразует объекты numpy, pandas и других специфических типов 
    в стандартные типы Python, пригодные для сериализации в JSON.
    
    Args:
        obj: Объект для преобразования
        
    Returns:
        Преобразованный объект
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if isinstance(k, (np.integer, np.floating)):
                try:
                    new_key = k.item()
                except (AttributeError, ValueError):
                    new_key = str(k)
            elif isinstance(k, (pd.Timestamp, pd.Timedelta)) or hasattr(k, 'isoformat'):
                try:
                    new_key = k.isoformat()
                except Exception:
                    new_key = str(k)
            elif not isinstance(k, (str, int, float, bool)) or k is None:
                new_key = str(k)
            else:
                new_key = k
            new_dict[new_key] = convert_numpy_types(v)
        return new_dict
    
    if isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    
    if isinstance(obj, np.integer):
        return int(obj)
    
    if isinstance(obj, np.floating):
        if np.isnan(obj) or np.isinf(obj):
            return str(obj)
        return float(obj)
    
    if isinstance(obj, np.bool_):
        return bool(obj)
    
    if isinstance(obj, np.str_):
        return str(obj)
    
    if isinstance(obj, np.ndarray):
        try:
            if obj.ndim == 0:
                return convert_numpy_types(obj.item())
            return obj.tolist()
        except Exception:
            return str(obj)
    
    if isinstance(obj, (pd.Timestamp, pd.Timedelta)):
        try:
            return obj.isoformat()
        except Exception:
            return str(obj)
    
    if hasattr(obj, 'isoformat'):
        try:
            return obj.isoformat()
        except Exception:
            return str(obj)
    
    return obj

