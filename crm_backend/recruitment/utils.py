from datetime import datetime


def generate_logo_path(instance, filename):
    """
    Генерирует путь сохранения загружаемой картинки.

    Возвращает путь сохранения картинки.
    """
    company_name = instance.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"images/company_logos/{company_name}/{timestamp}__{filename}"

def upload_to_candidates(instance, filename):
    """
    Генерирует путь сохранения загружаемых резюме и фотографий.

    Возвращает путь сохранения файлов.
    """
    if filename.endswith('.pdf'):
        return f"candidates/{instance.last_name}{instance.first_name}/resumes/{filename}"
    else:
        return f"candidates/{instance.last_name}{instance.first_name}/photos/{filename}"
    
