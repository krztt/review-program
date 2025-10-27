from tkinter import *
import tkinter as tk
from tkinter.constants import RIGHT
from tkinter.filedialog import asksaveasfile, askopenfilename
import PyPDF2
from tkinter import PhotoImage
from to_do_list import show_todo_mode 


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file: str):
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content if content else "")
        return pdf_text

# Function to save text to a file
def saveFile():
    new_file = asksaveasfile(mode='w', defaultextension=".txt", filetypes=[('Text files', '*.txt')])
    if new_file is None:
        return
    text = str(entry.get(1.0, tk.END))
    new_file.write(text)
    new_file.close()

# Function to open an existing text file
def openFile():
    file_path = askopenfilename(defaultextension=".txt", filetypes=[('Text files', '*.txt')])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        entry.delete(1.0, tk.END)  # Clear existing text in the entry box
        entry.insert(tk.INSERT, content)

# Function to clear the content in the text box
def clearFile():
    entry.delete(1.0, END)

# Function to convert PDF to text and display it in the text box
def pdfToTxt():
    file_path = askopenfilename(defaultextension=".pdf", filetypes=[('PDF files', '*.pdf')])
    if file_path:
        pdf_text = extract_text_from_pdf(file_path)
        entry.delete(1.0, tk.END)
        entry.insert(tk.INSERT, "\n".join(pdf_text))  # Join and insert the extracted text

# Timer Functions
timer_running = False
time_left = 0  # Starting time for the countdown in seconds (1 hour)
rest_time_left = 0
def update_timer():
    global time_left
    if time_left > 0 and timer_running:
        hours, remainder = divmod(time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        time_left -= 1
        canvas.after(1000, update_timer)  # Update every second
    elif time_left == 0:
        timer_label.config(text="It is time to rest")
        stop_timer()  # Automatically stop the timer when it hits zero

def start_timer():
    global timer_running, time_left, rest_time_left
    rest_time_left = 0
    time_left = 1500
    if not timer_running:
        timer_running = True
        update_timer()  # Start updating the timer
        start_button.config(state=DISABLED)
        rest_button.config(state=DISABLED)

def stop_timer():
    global timer_running
    timer_running = False
    start_button.config(state=NORMAL)
    rest_button.config(state=NORMAL)


# def reset_timer():
#     global time_left, timer_running
#     time_left = 1500  # Reset to 25 minutes (3600 seconds)
#     timer_label.config(text="00:25:00")
#     stop_timer()
def rest_update():
    global rest_time_left
    if  rest_time_left > 0 and timer_running:
        hours, remainder = divmod(rest_time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        rest_time_left -= 1
        canvas.after(1000, rest_update)  # Update every second
    elif rest_time_left == 0:
        timer_label.config(text="Let's get back to work")
        stop_timer()

def rest_timer():
    global rest_time_left, timer_running, time_left
    time_left = 0
    rest_time_left = 300
    if not timer_running:
        timer_running = True
        rest_update()  # Start updating the timer
        rest_button.config(state=DISABLED)
def resume_timer():
    global timer_running
    if not timer_running:
        timer_running = True
        if time_left > 0:
            start_button.config(state=DISABLED)
            update_timer()  # Continue from the work timer
        elif rest_time_left > 0:
            rest_update()
            rest_button.config(state=DISABLED)



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

def revert_style():
    try:
        selected_text = entry.tag_ranges("sel")  # Get the selected text range
        if selected_text:
            # Remove the styles by removing the tags
            entry.tag_remove("bold", selected_text[0], selected_text[1])
            entry.tag_remove("underline", selected_text[0], selected_text[1])
            entry.tag_remove("highlight", selected_text[0], selected_text[1])
            print("Styles reverted.")
    except Exception as e:
        print(f"Error reverting style: {e}")


# Set up the tkinter window
canvas = tk.Tk()
canvas.geometry('400x600')
canvas.title('Reviewer')
canvas.config(bg='white')

# Frame for buttons
top = Frame(canvas)
top.pack(padx=10, pady=5, anchor='nw')

#load images
open_image = PhotoImage(file='icons/Icons/open file.png') 
save_image = PhotoImage(file='icons/Icons/Untitled 07-27-2025 09-57-34.png')
clear_image = PhotoImage(file='icons/Icons/clear.png')
exit_image = PhotoImage(file='icons/Icons/exit.png')
pdf_image = PhotoImage(file='icons/Icons/pdf to text.png')
To_do_image = PhotoImage(file='icons/Icons/to do list.png')
return_image = PhotoImage(file='icons/Icons/return.png')



# Example for Open button
open_frame = Frame(top, bg='#f2a65e')
open_frame.pack(side=LEFT, padx=0)

b1 = Button(open_frame, image=open_image, borderwidth=0, highlightthickness=0, bg='#f2a65e', activebackground='#f2a65e', command=openFile)
b1.pack()
open_label = Label(open_frame, text='Open', bg='#f2a65e', fg='black', font=("Poppins", 10))
open_label.pack()

# Repeat for other buttons:
save_frame = Frame(top, bg='#f2a65e')
save_frame.pack(side=LEFT, padx=0)
b2 = Button(save_frame, image=save_image, borderwidth=0, highlightthickness=0, bg='#f2a65e', activebackground='#f2a65e', command=saveFile)
b2.pack()
save_label = Label(save_frame, text='Save', bg='#f2a65e', fg='black', font=("Poppins", 10))
save_label.pack()

clear_frame = Frame(top, bg='#f2a65e')
clear_frame.pack(side=LEFT, padx=0)
b3 = Button(clear_frame, image=clear_image, borderwidth=0, highlightthickness=0, bg='#f2a65e', activebackground='#f2a65e', command=clearFile)
b3.pack()
clear_label = Label(clear_frame, text='Clear', bg='#f2a65e', fg='black', font=("Poppins", 10))
clear_label.pack()

exit_frame = Frame(top, bg='#f2a65e')
exit_frame.pack(side=LEFT, padx=0)
b4 = Button(exit_frame, image=exit_image, borderwidth=0, highlightthickness=0, bg='#f2a65e', activebackground='#f2a65e', command=canvas.quit)  
b4.pack()
exit_label = Label(exit_frame, text='Exit', bg='#f2a65e', fg='black', font=("Poppins", 10))
exit_label.pack()

pdf_frame = Frame(top, bg='#f2a65e')
pdf_frame.pack(side=LEFT, padx=0)
b5 = Button(pdf_frame, image=pdf_image, borderwidth=0, highlightthickness=0, bg='#f2a65e', activebackground='#f2a65e', command=pdfToTxt)
b5.pack()
pdf_label = Label(pdf_frame, text='PDF to Text', bg='#f2a65e', fg='black', font=("Poppins", 10))
pdf_label.pack()

#timer_image
start_image = PhotoImage(file='icons/Icons/Untitled 07-27-2025 10-12-56.png')
stop_image = PhotoImage(file='icons/Icons/pause timer.png')    
rest_image = PhotoImage(file='icons/Icons/rest timer.png')
resume_image = PhotoImage(file='icons/Icons/Untitled 07-27-2025 10-12-56.png')


# Timer buttons (styled like file operation buttons)
timer_frame = Frame(top, bg='#f2a65e')
timer_frame.pack(side=LEFT, padx=0)  # Add some space from file buttons

# Start Timer
start_frame = Frame(timer_frame, bg='#f2a65e')
start_frame.pack(side=LEFT, padx=0)
start_button = Button(
    start_frame,
    image=start_image,
    borderwidth=0,
    highlightthickness=0,
    bg='#f2a65e',
    activebackground='#f2a65e',
    command=start_timer
)
start_button.pack()
start_label = Label(start_frame, text='Start', bg='#f2a65e', fg='black', font=("Poppins", 10))
start_label.pack()

# Stop Timer
stop_frame = Frame(timer_frame, bg='#f2a65e')
stop_frame.pack(side=LEFT, padx=0)
stop_button = Button(
    stop_frame,
    image=stop_image,
    borderwidth=0,
    highlightthickness=0,
    bg='#f2a65e',
    activebackground='#f2a65e',
    command=stop_timer
)
stop_button.pack()
stop_label = Label(stop_frame, text='Stop', bg='#f2a65e', fg='black', font=("Poppins", 10))
stop_label.pack()

# Rest Timer
rest_frame = Frame(timer_frame, bg='#f2a65e')
rest_frame.pack(side=LEFT, padx=0)
rest_button = Button(
    rest_frame,
    image=rest_image,
    borderwidth=0,
    highlightthickness=0,
    bg='#f2a65e',
    activebackground='#f2a65e',
    command=rest_timer
)
rest_button.pack()
rest_label = Label(rest_frame, text='Rest', bg='#f2a65e', fg='black', font=("Poppins", 10))
rest_label.pack()

# Resume Timer
resume_frame = Frame(timer_frame, bg='#f2a65e')
resume_frame.pack(side=LEFT, padx=0)
resume_button = Button(
    resume_frame,
    image=resume_image,
    borderwidth=0,
    highlightthickness=0,
    bg='#f2a65e',
    activebackground='#f2a65e',
    command=resume_timer
)
resume_button.pack()
resume_label = Label(resume_frame, text='Resume', bg='#f2a65e', fg='black', font=("Poppins", 10))
resume_label.pack()

# Timer display (styled for consistency)
timer_display_frame = Frame(timer_frame, bg='#f2a65e')
timer_display_frame.pack(side=LEFT, padx=10)
timer_label = Label(timer_display_frame, text="00:25:00", font=("Helvetica", 24), bg='white')
timer_label.pack(pady=20)

#Icons paths



# Text box for file content
canvas.configure(bg='#f2a65e')
main_content_frame = Frame(canvas, bg='#f2a65e')
main_content_frame.pack(fill=BOTH, expand=True)

# Move your Text widget into a frame so it can be hidden/shown
editor_frame = Frame(main_content_frame, bg='#f2a65e')
editor_frame.pack(fill=BOTH, expand=True)
entry = Text(editor_frame, wrap=WORD, bg='#F9DDA4', font=("Poppins", 15))
entry.pack(padx=10, pady=5, expand=True, fill=Y)

entry.tag_configure("bold", font=("Poppins", 15, "bold"))
entry.tag_configure("underline", font=("Poppins", 15, "underline"))
entry.tag_configure("highlight", background="yellow")

highlight_button = Button(canvas, text="Highlight", command=lambda: apply_selected_style("highlight"))
highlight_button.pack( padx = 5,pady=5, side = RIGHT)

underline_button = Button(canvas, text="Underline", command=lambda: apply_selected_style("underline"))
underline_button.pack(padx = 5,pady=5, side = RIGHT)

bold_button = Button(canvas, text="Bold", command=lambda: apply_selected_style("bold"))
bold_button.pack(padx = 5,pady=5, side = RIGHT)

revert_text = Button(canvas, text="revert text", command= revert_style)
revert_text.pack(padx = 5,pady=5, side = RIGHT)

# Create the to-do-list frame but don't pack it yet
todo_frame = show_todo_mode(main_content_frame)
todo_frame.pack_forget()  # Hide initially

def show_editor_mode():
    todo_frame.pack_forget()
    editor_frame.pack(fill=BOTH, expand=True)

def show_todo_mode_btn():
    editor_frame.pack_forget()
    todo_frame.pack(fill=BOTH, expand=True)

# Add a button to switch modes (put this with your other top buttons)

# To-Do List mode button with image
todo_mode_frame = Frame(top, bg='#f2a65e')
todo_mode_frame.pack(side=LEFT, padx=0)
todo_mode_btn = Button(
    todo_mode_frame,
    image=To_do_image,
    borderwidth=0,
    highlightthickness=0,
    bg='#f2a65e',
    activebackground='#f2a65e',
    command=show_todo_mode_btn
)
todo_mode_btn.pack()
todo_mode_label = Label(todo_mode_frame, text='To-Do List', bg='#f2a65e', fg='black', font=("Poppins", 10))
todo_mode_label.pack()

# Editor mode button with image (use return_image)
editor_mode_frame = Frame(top, bg='#f2a65e')
editor_mode_frame.pack(side=LEFT, padx=0)
editor_mode_btn = Button(
    editor_mode_frame,
    image=return_image,
    borderwidth=0,
    highlightthickness=0,
    bg='#f2a65e',
    activebackground='#f2a65e',
    command=show_editor_mode
)
editor_mode_btn.pack()
editor_mode_label = Label(editor_mode_frame, text='Editor', bg='#f2a65e', fg='black', font=("Poppins", 10))
editor_mode_label.pack()

# Key bindings for buttons
canvas.bind('<Control-h>', lambda event: highlight_button.invoke())
canvas.bind('<Control-u>', lambda event: underline_button.invoke())
canvas.bind('<Control-b>', lambda event: bold_button.invoke())
canvas.bind('<Control-r>', lambda event: revert_style())
# Run the Tkinter event loop
canvas.mainloop()
