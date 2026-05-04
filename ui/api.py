import logging
import time
from typing import Dict, List

import requests

logger = logging.getLogger('ui.api')
API_BASE_URL = 'http://127.0.0.1:8001'


def fetch_chat_history(limit: int = 20) -> List[Dict]:
    try:
        start_time = time.time()
        response = requests.get(f'{API_BASE_URL}/history', params={'limit': limit}, timeout=6)
        response.raise_for_status()
        history = response.json()

        seen_messages = set()
        unique_history = []
        for entry in history:
            message = entry.get('message', '')
            if message not in seen_messages:
                seen_messages.add(message)
                unique_history.append(entry)

        logger.info(
            f'Loaded history in {time.time() - start_time:.2f}s: {len(history)} records, {len(unique_history)} unique'
        )
        return unique_history

    except requests.RequestException as exc:
        logger.error(f'Failed to load history: {exc}')
        return []


def clear_saved_history() -> bool:
    try:
        response = requests.delete(f'{API_BASE_URL}/history', timeout=6)
        if response.status_code == 200:
            logger.info('Saved chat history cleared successfully')
            return True
        logger.warning(f'Failed to clear history: HTTP {response.status_code}')
        return False
    except requests.RequestException as exc:
        logger.error(f'Error clearing history: {exc}')
        return False


def check_backend_health() -> str:
    try:
        response = requests.get(f'{API_BASE_URL}/health', timeout=5)
        if response.status_code == 200:
            return 'healthy'
        return 'warning'
    except requests.RequestException:
        return 'offline'


def get_ai_response(question: str) -> str:
    try:
        start_time = time.time()
        response = requests.get(f'{API_BASE_URL}/ask', params={'question': question}, timeout=60)
        response.raise_for_status()
        data = response.json()
        logger.info(f'Backend answered in {time.time() - start_time:.2f}s')
        return data.get('response', 'No answer returned from backend.')
    except requests.RequestException as exc:
        logger.error(f'AI response error: {exc}')
        raise
