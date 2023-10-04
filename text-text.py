# Import the g4f module, assuming it's a library used for some specific functionality.
import g4f

# Automatic selection of provider

# Streamed completion:
# Create a chat conversation with the GPT-3.5 Turbo model and provide a user message.
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Compose a compelling Amazon product description focusing on the provided keywords, and format the product features using bullet points: a close up of a smart watch; Noise ColorFit Pulse 3, 1.96' Display, Men and Women, Smart watch",
        }
    ],
    stream=True,
)

# Iterate through the response and print each message.
for message in response:
    print(message, flush=True, end='')
