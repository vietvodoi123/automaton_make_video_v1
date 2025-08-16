
# audio
import asyncio
from processors import audio_process, text_process,create_video_with_task_id
from dispatcher.dispatcher import dispatch_tasks

dispatch_tasks()
for i in range(1, 6):
    task_id = f"t17_part{i}"
    text_process(task_id)
    asyncio.run(audio_process(task_id))
    create_video_with_task_id(task_id)

# for i in range(51, 56):
#     task_id = f"t13_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)


# for i in range(11, 15):
#     task_id = f"t11_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)


# for i in range(31, 36):
#     task_id = f"t14_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)
#
# for i in range(11, 16):
#     task_id = f"t12_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)


# kenh 2
# for i in range(11, 16):
#     task_id = f"t6_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)
# dispatch_tasks()
# for i in range(6, 10):
#     task_id = f"t16_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)

# for i in range(6, 10):
#     task_id = f"t15_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)