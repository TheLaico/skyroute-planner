import json

class JSONLoader:
    """
    Cargador de archivos JSON para la red de aeropuertos y rutas.
    """
    @staticmethod
    def load(filepath: str) -> dict:
        """
        Carga y valida un archivo JSON. Debe contener las claves 'airports' y 'routes' y al menos 30 aeropuertos.
        :param filepath: Ruta al archivo JSON.
        :return: Diccionario con los datos validados.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'airports' not in data or 'routes' not in data:
            raise ValueError("El archivo debe contener las claves 'airports' y 'routes'.")
        if len(data['airports']) < 30:
            raise ValueError("Debe haber al menos 30 aeropuertos en la red.")
        return data

    @staticmethod
    def get_global_config(data: dict) -> dict:
        """
        Extrae la sección 'config' del archivo, o retorna valores por defecto si no existe.
        :param data: Diccionario de datos cargados.
        :return: Diccionario de configuración global.
        """
        return data.get('config', {"max_budget": 10000, "max_time_min": 10000})
