import tkinter as tk

# Initialize Tkinter window
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Create a Text widget
entry = tk.Text(canvas, wrap="word", bg='#F9DDA4', font=("Poppins", 15))
entry.pack(padx=10, pady=5, expand=True, fill="y")

# Insert some sample text
entry.insert("1.0", "This is some text. Feel free to manipulate it. Select and style the text!")

# Create tags for styles
entry.tag_configure("bold", font=("Poppins", 15, "bold"))
entry.tag_configure("underline", font=("Poppins", 15, "underline"))
entry.tag_configure("highlight", background="yellow")


# Function to apply styles to selected text
def apply_selected_style(style):
    try:
        # Get the selected text's range (start and end indices)
        start_index = entry.index("sel.first")
        end_index = entry.index("sel.last")

        # Apply the selected style
        entry.tag_add(style, start_index, end_index)
    except tk.TclError:
        # Handle the case where no text is selected (raises TclError)
        print("No text selected!")


# Create a Button to apply bold to selected text
bold_button = tk.Button(root, text="Bold", command=lambda: apply_selected_style("bold"))
bold_button.pack(pady=5)

# Create a Button to apply underline to selected text
underline_button = tk.Button(root, text="Underline", command=lambda: apply_selected_style("underline"))
underline_button.pack(pady=5)

# Create a Button to apply highlight to selected text
highlight_button = tk.Button(root, text="Highlight", command=lambda: apply_selected_style("highlight"))
highlight_button.pack(pady=5)

root.mainloop()
