
def get_response_open_ai(client,prompt):
    response =  client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            max_tokens=600,
            temperature=0,
            stream=True
        )
    for chunk in response:
            content = chunk.choices[0].delta.content
            if content is not None:
                yield f"{content}"



def get_parse_response_open_ai(client,prompt,format_model):
    response =  client.chat.completions.parse(
    model="gpt-4o",
    messages=prompt,
    response_format=format_model
    )

    return response

def create_baseline_prompt(frames,exercise_name="squat"):
    """Create a prompt for baseline analysis (frames only)."""
    prompt_messages = [
        {
            "role": "user",
            "content": [
                f"These frames represent various points in a {exercise_name} exercise. Analyze the  form based solely on visual information from these frames. Provide advice based on what you observe.",
                *map(lambda x: {"image": x}, frames)
            ],
        }
    ]
    return prompt_messages


def _parse_conversation_history(conversation_history):
     """Parse the conversation history into a list a String"""
     full_conversation = "" 
     for message in conversation_history:
        conversation_message = f"{message['sender']} said: '{message['text']}' on {message['timestamp']}\n"
        full_conversation += conversation_message
     return full_conversation


def create_prompt(conversation):
    """Create a prompt for baseline analysis (frames only)."""
    system_prompt = "You are a personal trainer and nutritionist. You will answer the user's questions and provide advice based on the conversation history."
    user_prompt = conversation.message
    if conversation.conversationHistory:
        conversation_history = _parse_conversation_history(conversation.conversationHistory)
        user_prompt += f"\n\nConversation history:\n{conversation_history}"
    prompt_messages = [
         {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    return prompt_messages



def create_user_workout_plan_prompt(user):
    """Create a prompt for baseline analysis (frames only)."""
    system_prompt = "Generate a workout plan with three workouts, with maximum 4 exercises in each workout the specified format, based on the goals of the user. If the exercise category is Weightlifting, include weight in kilos and number of repetitions. If the exercise category is Bodyweight, include only repetitions. If the exercise category is cardio or flexibility, include only duration in minutes. The video URL is very necessary, and must link to an actual video or animation. You can also use .gif. If the video is from youtube, please use the youtube embed url, as these videos will be displayed in a website. Do not use example.com. Use youtube if possible."
    user_prompt = f"Create a workout plan for me. I am {user.gender}, weigh {user.weight} kilograms, {user.height} centimeters tall, and my goal is to {user.goal}"
    base_input = [
    {"role":"system", "content":system_prompt},
    {"role":"user","content":user_prompt}
] 
    return base_input



def create_user_meal_plan_prompt(user):
    """Create a prompt for baseline analysis (frames only)."""
    system_prompt = "Generate a meal plan based on the goals of the user for three days, with three meals per day. The recipe url for the meal is important and should be obtained from recipes from the internet. The recipe url must point to a real page that includes a recipe of the meal. The description should include nutrient facts and key ingredients."
    user_prompt = f"Create a meal plan for me. I am {user.gender}, weigh {user.weight} kilograms, {user.height} centimeters tall, and my goal is to {user.goal}"
    base_input = [
    {"role":"system", "content":system_prompt},
    {"role":"user","content":user_prompt}
] 
    return base_input






