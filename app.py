import gradio as gr

def my_function(name):
    return f"Hello {name}! Welcome to my first app! 🎉"

demo = gr.Interface(
    fn=my_function,
    inputs=gr.Textbox(label="What's your name?"),
    outputs=gr.Textbox(label="My app says:"),
    title="My First App",
    description="Type your name and see what happens!"
)

if __name__ == "__main__":
    demo.launch()
