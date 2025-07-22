
# audio
import asyncio
from processors import audio_process, text_process,create_video_with_task_id


for i in range(4, 11):
    task_id = f"t1_part{i}"
    text_process(task_id)
    asyncio.run(audio_process(task_id))
    create_video_with_task_id(task_id)