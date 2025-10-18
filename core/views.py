from django.shortcuts import render
import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
import requests
from requests import RequestException
from rest_framework.decorators import api_view
from rest_framework.response import Response

load_dotenv()  # loads .env file

logger = logging.getLogger(__name__)

CAT_FACT_URL = "https://catfact.ninja/fact"
CAT_FACT_TIMEOUT_SECONDS = 5

def _get_cat_fact(timeout=CAT_FACT_TIMEOUT_SECONDS):
    try:
        resp = requests.get(CAT_FACT_URL, timeout=timeout)
        resp.raise_for_status()
        j = resp.json()
        fact = j.get('fact')
        if isinstance(fact, str) and fact.strip():
            return fact.strip()
        logger.warning("Cat fact response did not contain 'fact' field: %s", j)
        return None
    except RequestException as e:
        logger.exception("Error fetching cat fact: %s", e)
        return None

def _iso_utc_now():
    # ISO 8601 with milliseconds and trailing Z (no offset)
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

@api_view(['GET'])
def profile_view(request):
    """
    GET /me
    Returns:
      {
        "status": "success",
        "user": { "email": "...", "name": "...", "stack": "..." },
        "timestamp": "<UTC ISO 8601>",
        "fact": "<cat fact or fallback>"
      }
    """
    # Load profile values from environment, defaults provided
    email = os.getenv('PROFILE_EMAIL')
    name = os.getenv('PROFILE_NAME' )
    stack = os.getenv('PROFILE_STACK')

    cat_fact = _get_cat_fact()
    if not cat_fact:
        cat_fact = "Cat fact unavailable at the moment. Please try again later."

    payload = {
        "status": "success",
        "user": {
            "email": email,
            "name": name,
            "stack": stack
        },
        "timestamp": _iso_utc_now(),
        "fact": cat_fact
    }

    # Return with DRF Response; content-type will be application/json
    return Response(payload, status=200)
