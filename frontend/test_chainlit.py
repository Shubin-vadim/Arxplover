import chainlit as cl
from chainlit.types import ThreadDict

@cl.step(type="tool")
async def tool(message: cl.Message):
    # Fake tool
    await cl.sleep(2)
    return f"Response from the tool! {message.content}"

# @cl.on_chat_start
# async def on_chat_start():
#     # print("A new chat session has started!")
#     await cl.Message(content='Hi').send()
#     cl.user_session.set("counter", 0)

@cl.on_stop
async def on_stop():
    await cl.Message(content='The user wants to stop the task!').send()

@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print("The user resumed a previous chat session!")


# @cl.set_starters
# async def set_starters():
#     return [
#         cl.Starter(
#             label="Morning routine ideation",
#             message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
#             icon="https://avatars.mds.yandex.net/i?id=82492638aa0b99045b77c56d3127852776c472a8-5680793-images-thumbs&n=13",
#             ),

#         cl.Starter(
#             label="Explain superconductors",
#             message="Explain superconductors like I'm five years old.",
#             icon="/public/learn.svg",
#             ),
#         cl.Starter(
#             label="Python script for daily email reports",
#             message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
#             icon="/public/terminal.svg",
#             ),
#         cl.Starter(
#             label="Text inviting friend to wedding",
#             message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
#             icon="https://avatars.mds.yandex.net/i?id=859d506b27e960f2b03bcafecd96cc84a501c912-10908937-images-thumbs&n=13",
#             )
#         ]
# ...

# @cl.set_chat_profiles
# async def chat_profile(current_user: cl.User):
#     if current_user.metadata["role"] != "ADMIN":
#         return None

#     return [
#         cl.ChatProfile(
#             name="My Chat Profile",
#             icon="https://picsum.photos/250",
#             markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
#             starters=[
#                 cl.Starter(
#                     label="Morning routine ideation",
#                     message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
#                     icon="/public/idea.svg",
#                 ),
#                 cl.Starter(
#                     label="Explain superconductors",
#                     message="Explain superconductors like I'm five years old.",
#                     icon="/public/learn.svg",
#                 ),
#             ],
#         )
#     ]


# @cl.on_message  # this function will be called every time a user inputs a message in the UI
# async def main(message: cl.Message):
#     """
#     This function is called every time a user inputs a message in the UI.
#     It sends back an intermediate response from the tool, followed by the final answer.

#     Args:
#         message: The user's message.

#     Returns:
#         None.
#     """

#     # counter = cl.user_session.get("counter")
#     # counter += 1
#     # cl.user_session.set("counter", counter)

#     # image = cl.Image(path="imgs\\arhitect_1.png", name="image1", display="inline")
#     # image = cl.Image(path="imgs\\arhitect_1.png", name="image1", display="side")
#     image = cl.Image(path="imgs\\arhitect_1.png", name="image1", display="page")
#     # Call the tool
#     tool_res = await tool(message)

#     print(cl.chat_context.to_openai())

#     await cl.Message(content=tool_res, elements=[image]).send()

@cl.action_callback("action_button")
async def on_action(action: cl.Action):
    print(action.payload)

@cl.on_message
async def on_message(msg: cl.Message):
    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return
    print(msg.elements)
    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]
    # print(images[0].name)
    print(images)

    # Read the first image
    with open(images[0].path, "r") as f:
        pass

    await cl.Message(content=f"Received {len(images)} image(s)").send()

@cl.on_chat_start
async def start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(
            name="action_button",
            icon="mouse-pointer-click",
            payload={"value": "example_value"},
            label="Click me!"
        )
    ]

    await cl.Message(content="Interact with this action button:", actions=actions).send()