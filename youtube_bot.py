## take input of video link 
## use the youtube api to get the transcript
## append the transcript to the messages array
## respond with ask any questions 
## take a question as input and answer 

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import openai
import gradio

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "No transcript found for this video."
    except Exception as e:
        return f"An error occurred: {e}"

openai.api_key = "####"

# Initialize state
state = {"is_link": True, "transcript": ""}

messages = [{"role": "system", "content": "You are an agent that takes in Youtube video transcripts and adeptly answers any following questions the user may have"}]

def CustomChatGPT(user_input):
    if state["is_link"]:
        # Handle YouTube link input
        video_id = user_input.split("v=")[-1]  # Extract video ID from URL
        transcript = get_transcript(video_id)
        messages.append({"role": "user", "content": transcript})
        response = "Link is ready, shoot your questions!"
        state["is_link"] = False
        return response

    else:
        messages.append({"role": "user", "content": user_input})    
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "user", "content": ChatGPT_reply})
        return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs = "text", outputs = "text", title = "Youtube Summariser")

demo.launch(share=True)





