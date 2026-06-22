import os
import sys
import asyncio
import socket
import threading

# Set environment variables as early as possible
os.environ["RAGAS_DO_NOT_TRACK"] = "True"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

# Early DNS resolution of api.openai.com before native DLLs/thread pools are loaded
try:
    _openai_resolved = socket.getaddrinfo('api.openai.com', 443)
except Exception:
    _openai_resolved = [
        (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('172.66.0.243', 443)),
        (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('162.159.140.245', 443))
    ]

# Thread-safe lock wrapper around _socket.getaddrinfo to prevent concurrent Windows socket resolution crashes
import _socket
_original_getaddrinfo = _socket.getaddrinfo
_getaddrinfo_lock = threading.Lock()

def _locked_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    print(f"  [getaddrinfo] (tests) Bypassing native resolve for: {host}:{port}", flush=True)
    
    if host == 'api.openai.com':
        res = []
        for fam, socktype, prot, canon, sa in _openai_resolved:
            new_sa = (sa[0], port) + sa[2:]
            res.append((fam, socktype or type, prot or proto, canon, new_sa))
        return res
        
    if host in ('127.0.0.1', 'localhost'):
        return [
            (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', port))
        ]
        
    with _getaddrinfo_lock:
        return _original_getaddrinfo(host, port, family, type, proto, flags)

_socket.getaddrinfo = _locked_getaddrinfo
socket.getaddrinfo = _locked_getaddrinfo
print("CONFTEST: Thread-safe _socket.getaddrinfo bypass initialized.", flush=True)
