import chainlit as cl

@cl.on_message
async def main(msg: cl.Message) -> None:

    content = ""
    image_extensions = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']

    if not msg.elements:
        match msg.elements[0].mime:
            case 'application/pdf':
                pass
            case mine if mine in image_extensions:
                pass
            case _:
                pass
    else:
        pass

    await cl.Message(content=content).send()
