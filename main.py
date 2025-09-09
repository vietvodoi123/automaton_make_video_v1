
# audio
import asyncio
from processors import audio_process, text_process,create_video_with_task_id
from dispatcher.dispatcher import dispatch_tasks


# a=["t14_part1502"]
# for i in a:
#     text_process(i)
#     asyncio.run(audio_process(i))
#     create_video_with_task_id(i)

# 99 - 106

# for i in range(152, 156):
#     task_id = f"t14_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)
# # dispatch_tasks()
#
# for i in range(91, 96):
#     task_id = f"t18_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)
for i in range(40, 41):
    task_id = f"t19_part{i}"
    text_process(task_id)
    asyncio.run(audio_process(task_id))
    create_video_with_task_id(task_id)
# #
# for i in range(11, 21):
#     task_id = f"t17_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)

# for i in range(61, 64):
#     task_id = f"t13_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)


# for i in range(11, 15):
#     task_id = f"t11_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)



#
# for i in range(46, 51):
#     task_id = f"t12_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)
# for i in range(56, 61):
#     task_id = f"t14_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)

# kenh 2
# for i in range(41, 46):
#     task_id = f"t6_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)
# dispatch_tasks()
# for i in range(36, 41):
#     task_id = f"t16_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)

# for i in range(6, 10):
#     task_id = f"t15_part{i}"
#     text_process(task_id)
#     asyncio.run(audio_process(task_id))
#     create_video_with_task_id(task_id)


# sua chua

