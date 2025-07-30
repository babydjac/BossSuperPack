/# Parse models response/,/system_prompt/ c\
        # Parse models response, supporting both 'results' and 'data' keys per the API docs\
        models_list = None\
        if isinstance(data, dict):\
            models_list = data.get('results') or data.get('data')\
        elif isinstance(data, list):\
            models_list = data\
        else:\
            raise ValueError(f'Unexpected response structure: {type(data)}')\
        if not models_list:\
            raise ValueError('No models found in response')\
        # If list of dicts, grab their IDs; otherwise assume it’s already a list of strings\
        if isinstance(models_list[0], dict):\
            available = [m['id'] for m in models_list]\
        else:\
            available = models_list
