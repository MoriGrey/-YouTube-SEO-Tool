"""
Performance Optimization Script
Optimizes the system for large datasets
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def optimize_json_files():
    """Optimize JSON data files by removing old entries."""
    print("[1] Optimizing JSON data files...")
    
    data_dir = Path("data")
    if not data_dir.exists():
        print("  [SKIP] Data directory does not exist")
        return
    
    optimized = 0
    max_entries = 1000  # Keep only last 1000 entries
    
    for json_file in data_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            original_size = len(str(data))
            modified = False
            
            # Optimize lists (keep only recent entries)
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > max_entries:
                        data[key] = value[-max_entries:]
                        modified = True
                        print(f"  - {json_file.name}: Trimmed {key} from {len(value)} to {max_entries} entries")
            
            if modified:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                new_size = len(str(data))
                saved = original_size - new_size
                print(f"  [OK] {json_file.name}: Saved {saved:,} bytes")
                optimized += 1
        
        except Exception as e:
            print(f"  [WARN] {json_file.name}: {str(e)}")
    
    if optimized > 0:
        print(f"  [OK] Optimized {optimized} files")
    else:
        print("  [INFO] No files needed optimization")

def check_cache_performance():
    """Check and optimize cache performance."""
    print("[2] Checking cache performance...")
    
    cache_dir = Path(".cache")
    if not cache_dir.exists():
        print("  [INFO] Cache directory does not exist (will be created on first use)")
        return
    
    total_size = 0
    file_count = 0
    
    for cache_file in cache_dir.rglob("*"):
        if cache_file.is_file():
            total_size += cache_file.stat().st_size
            file_count += 1
    
    if file_count > 0:
        size_mb = total_size / (1024 * 1024)
        print(f"  [INFO] Cache: {file_count} files, {size_mb:.2f} MB")
        
        if size_mb > 100:  # If cache > 100MB
            print("  [WARN] Cache is large. Consider clearing old cache files.")
            print("         Run: find .cache -type f -mtime +7 -delete")
    else:
        print("  [INFO] Cache is empty")

def optimize_database_queries():
    """Suggest database query optimizations."""
    print("[3] Database query optimization suggestions...")
    
    suggestions = [
        "Use batch processing for multiple API calls",
        "Implement request rate limiting to avoid quota exhaustion",
        "Cache frequently accessed data",
        "Use pagination for large result sets",
        "Implement connection pooling for external APIs"
    ]
    
    print("  [INFO] Optimization suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"    {i}. {suggestion}")

def create_performance_config():
    """Create performance configuration file."""
    print("[4] Creating performance configuration...")
    
    config = {
        "cache": {
            "enabled": True,
            "ttl_seconds": 3600,
            "max_size_mb": 100,
            "cleanup_interval_hours": 24
        },
        "api": {
            "rate_limit_per_minute": 60,
            "batch_size": 10,
            "timeout_seconds": 30,
            "retry_attempts": 3
        },
        "data": {
            "max_entries_per_file": 1000,
            "cleanup_old_entries_days": 30,
            "compress_old_data": True
        },
        "performance": {
            "enable_multithreading": True,
            "max_workers": 5,
            "enable_async_requests": False
        }
    }
    
    config_file = Path("performance_config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"  [OK] Created {config_file}")

def main():
    """Run all performance optimizations."""
    print("=" * 60)
    print("Performance Optimization")
    print("=" * 60)
    print()
    
    optimize_json_files()
    print()
    check_cache_performance()
    print()
    optimize_database_queries()
    print()
    create_performance_config()
    print()
    
    print("=" * 60)
    print("[SUCCESS] Performance optimization completed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review performance_config.json")
    print("2. Monitor cache size regularly")
    print("3. Run this script periodically to clean up old data")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

