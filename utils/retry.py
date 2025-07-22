import time
import traceback
def retry_with_limit(max_retries, delay_sec, func, *args, **kwargs):
    """Hàm helper để thử lại tối đa N lần với delay"""
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Lỗi ở lần thử {attempt}/{max_retries}: {e}")
            traceback.print_exc()
            if attempt < max_retries:
                print(f"🔁 Thử lại sau {delay_sec} giây...")
                time.sleep(delay_sec)
            else:
                raise