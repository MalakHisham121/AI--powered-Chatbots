from graph import app

def run_bot():
    print("Inventory Bot Ready (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']: break
        config = {"configurable": {"thread_id": "1"}}
        for event in app.stream({"question": user_input}, config):
            if "responder" in event:
                print(f"Bot: {event['responder']['response']}")

if __name__ == "__main__":
    run_bot()
