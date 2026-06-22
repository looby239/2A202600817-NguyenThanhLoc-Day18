import os
import httpx
import time

snapshot_dir = os.path.expanduser('~/.cache/huggingface/hub/models--BAAI--bge-m3/snapshots/5617a9f61b028005a4858fdac845db406aefb181')
target_path = os.path.join(snapshot_dir, 'pytorch_model.bin')
url = "https://hf-mirror.com/BAAI/bge-m3/resolve/main/pytorch_model.bin"

print(f"Downloading {url} to {target_path}...", flush=True)
start_time = time.time()
try:
    with httpx.stream("GET", url, follow_redirects=True, timeout=600.0) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        print(f"Total size: {total_size / (1024*1024):.2f} MB", flush=True)
        downloaded = 0
        last_print = 0
        with open(target_path, "wb") as f:
            for chunk in r.iter_bytes(chunk_size=1024*1024*2): # 2MB chunks
                f.write(chunk)
                downloaded += len(chunk)
                if downloaded - last_print >= 100 * 1024 * 1024:
                    elapsed = time.time() - start_time
                    speed = downloaded / (1024*1024*elapsed) if elapsed > 0 else 0
                    print(f"Downloaded: {downloaded / (1024*1024):.2f} MB / {total_size / (1024*1024):.2f} MB ({downloaded/total_size*100:.1f}%) | Speed: {speed:.2f} MB/s", flush=True)
                    last_print = downloaded
    print(f"Finished downloading in {time.time() - start_time:.1f}s", flush=True)
except Exception as e:
    print(f"Error during download: {e}", flush=True)
