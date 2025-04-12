import json
import pandas as pd
import streamlit as st
import redis

# Initialize Redis client (default port 6379)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_data(user_id, key, value=None, ttl=None):
    """
    Cache data in Redis with optional TTL.
    
    Args:
        user_id: User identifier
        key: Cache key
        value: Data to cache
        ttl: Time to live in seconds (optional)
    """
    full_key = f"{user_id}:{key}"
    
    if isinstance(value, (list, dict)):
        value = json.dumps(value)  # Convert list or dict to a JSON string
    
    if ttl:
        redis_client.setex(full_key, ttl, str(value))  # Set with expiry
    else:
        redis_client.set(full_key, str(value))  # Set without expiry

def get_cached_data(user_id, key=None):
    """
    Get cached data from Redis.
    
    Args:
        user_id: User identifier or full cache key
        key: Cache key (optional, if user_id contains the full key)
    
    Returns:
        Cached data or None if not found
    """
    # If key is None, assume user_id is the full key
    full_key = f"{user_id}:{key}" if key else user_id
    
    value = redis_client.get(full_key)
    if value:
        try:
            return json.loads(value)  # Convert JSON string back to list or dict
        except json.JSONDecodeError:
            return value
    return None

def user_exists(user_id):
    """Check if a user exists in Redis."""
    return redis_client.exists(user_id)

def add_user(user_id):
    """Add a user to Redis."""
    redis_client.set(user_id, "exists")

def append_to_cache_list(user_id, key, value):
    """
    Append a value to a cached list.
    
    Args:
        user_id: User identifier
        key: Cache key
        value: Value to append
    """
    cached = get_cached_data(user_id, key)
    
    # Standardize the cached data structure
    if cached is None:
        new_data = [value]
    elif isinstance(cached, list):
        # If already a list, append to it
        new_data = cached + [value]
    elif isinstance(cached, dict):
        if isinstance(value, dict):
            new_data = [cached, value]
        else:
            new_data = [cached, {"value": value}]
    else:
        new_data = [cached, value]
    
    cache_data(user_id, key, new_data)