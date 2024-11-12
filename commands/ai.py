import aiohttp
import asyncio

class AICommand:
    # Attributes
    name = 'ai'
    description = 'Free AI Chatbot!'
    admin_bot = False
    version = '1.0.3'
    credits = 'Yan Maglinte'
    use_prefix = False
    command_category = 'chatbots'
    usages = 'Ai prompt!'
    cooldowns = 0

    async def execute(self, api, sender_id, thread_id, message_text, message_reply=None):
        prompt = message_text.strip()
        
        # Greet the user if no prompt is provided
        if not prompt:
            await api.send_message('Hello 👋 How can I help you today?', thread_id)
            return

        # Check if the message is a reply with an image attachment
        if message_reply and 'attachments' in message_reply:
            attachment = message_reply['attachments'][0]
            if attachment.get('type') == 'photo':
                image_url = attachment.get('url')

                # Send image-based prompt to API
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post('https://joshweb.click/gemini', json={
                            'prompt': prompt,
                            'credits': self.credits,
                            'image_url': image_url,
                        }) as response:
                            data = await response.json()
                            output = data.get('result', 'No response from the API')
                            await api.send_message(output, thread_id)
                except Exception as e:
                    print('Error:', e)
                    await api.send_message('⚠️ An error occurred!', thread_id)
                return

        # Standard text prompt handling (no image)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://joshweb.click/new/gemini', json={
                    'prompt': prompt,
                    'credits': self.credits,
                }) as response:
                    data = await response.json()
                    output = data.get('result', 'No response from the API')
                    await api.send_message(output, thread_id)
        except Exception as e:
            print('Error:', e)
            await api.send_message('⚠️ An error occurred!', thread_id)

# Example usage:
# Assuming `api.send_message` is a function that takes `message_text` and `thread_id`
# command = AICommand()
# asyncio.run(command.execute(api, sender_id="12345", thread_id="67890", message_text="Hello AI"))
