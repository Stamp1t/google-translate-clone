import customtkinter as ctk
import googletrans
from PIL import Image
from googletrans import Translator
from tkinter import filedialog

root = ctk.CTk()
root.geometry("1000x600")
root.title("Translator")

ctk.set_appearance_mode("light")

translate_font = ctk.CTkFont(family="Arial", size=20)

translator = Translator(service_urls=["translate.google.com"])

LANGUAGES = []
for language in googletrans.LANGCODES:
    LANGUAGES.append(language)

global start_translation_id
start_translation_id = None


# translates input and displays translated input in output box
def translate():
    phrase = input_box.get("0.0", "end")
    if len(phrase.strip()) > 0:
        trans_phrase = translator.translate(phrase, src=googletrans.LANGCODES[original_lang_selection.get()],
                                            dest=googletrans.LANGCODES[translated_lang_selection.get()]).text
        output_box.delete("0.0", index2="end")
        output_box.insert("0.0", trans_phrase)


def clear_input():
    input_box.delete("0.0", index2="end")
    char_counter_var.set("0/10000")


# gets called whenever a key is pressed
def handle_event_type(event):
    handle_translation()
    handle_char_count()


# starts translating if this functions was called at least once and then not again for 1 second -> auto translates
#  input if user stops typing
def handle_translation():
    global start_translation_id

    if start_translation_id is not None:
        root.after_cancel(start_translation_id)
    start_translation_id = root.after(1000, translate)


# simply a function which can be called if there is an unnecessary parameter
def change_translation(useless):
    translate()


# counts the amount of chars typed in the input box
def handle_char_count():
    char_counter_var.set(f"{len(input_box.get('0.0', 'end'))}/10000")


def switch_color_mode():
    if toggle_mode.get() == "dark":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")


# opens a txt file
def open_txt_file():
    path_to_file = filedialog.askopenfilename(filetypes=[("txt", "*txt")])
    with open(path_to_file, "r") as txt_file:
        input_box.delete("0.0", "end")
        input_box.insert(0.0, txt_file.read())
        translate()


# saves a txt file
def save_txt_file():
    path_to_file = filedialog.asksaveasfilename(filetypes=[("txt", "*txt")])
    with open(path_to_file, "w") as txt_file:
        txt_file.write(output_box.get("0.0", "end"))


# __________GUI____________
selected_original_lang_var = ctk.StringVar(value="german")
original_lang_selection = ctk.CTkOptionMenu(root, values=LANGUAGES, variable=selected_original_lang_var,
                                            command=change_translation, font=translate_font)
original_lang_selection.grid(column=1, row=0, pady=20, padx=30, sticky="wes")

selected_translated_lang_var = ctk.StringVar(value="english")
translated_lang_selection = ctk.CTkOptionMenu(root, values=LANGUAGES, variable=selected_translated_lang_var,
                                              command=change_translation, font=translate_font)
translated_lang_selection.grid(column=2, row=0, pady=20, padx=30, sticky="wes")

logo_image = ctk.CTkImage(Image.open("./images/translator.png"), size=(60, 60))
logo_label = ctk.CTkLabel(root, image=logo_image, text="")
logo_label.grid(column=0, row=0, pady=(20, 0))

options_frame = ctk.CTkFrame(root)
options_frame.grid(column=0, row=1, padx=30, pady=30, stick="nswe")

toggle_mode = ctk.CTkSwitch(options_frame, command=switch_color_mode, text="Dark Mode", onvalue="dark",
                            offvalue="light")
toggle_mode.pack(expand=True)

open_file_text = ctk.CTkLabel(options_frame, text="Import Text File")
open_file_text.pack()

open_file_button = ctk.CTkButton(options_frame, text="Open File", command=open_txt_file)
open_file_button.pack(expand=True, anchor="n", padx=25)

save_into_file_text = ctk.CTkLabel(options_frame, text="Save Text")
save_into_file_text.pack()

save_into_file_button = ctk.CTkButton(options_frame, text="Save File", command=save_txt_file)
save_into_file_button.pack(expand=True, anchor="n", padx=25)

original_text_frame = ctk.CTkFrame(root, fg_color=("white", "#1d1e1e"))
original_text_frame.grid(column=1, row=1, sticky="nswe", padx=30, pady=30)

input_box = ctk.CTkTextbox(original_text_frame, font=translate_font, border_width=0, fg_color=("white", "#1d1e1e"))
input_box.grid(column=0, row=0, columnspan=2, sticky="nswe", padx=(20, 0), pady=2)
input_box.bind("<Key>", handle_event_type)

delete_input_button = ctk.CTkButton(original_text_frame, text="X", width=1, command=clear_input, font=translate_font,
                                    corner_radius=350)
delete_input_button.grid(column=2, row=0, sticky="ne", padx=10, pady=10)

char_counter_var = ctk.StringVar()
char_counter_var.set("0/10000")
char_counter_input_box = ctk.CTkLabel(original_text_frame, textvariable=char_counter_var, font=translate_font)
char_counter_input_box.grid(column=1, row=1, columnspan=2, padx=15, sticky="ne")

translated_text_frame = ctk.CTkFrame(root, fg_color=("white", "#1d1e1e"))
translated_text_frame.grid(column=2, row=1, sticky="nswe", padx=30, pady=30)

output_box = ctk.CTkTextbox(translated_text_frame, border_width=0, font=translate_font, fg_color=("white", "#1d1e1e"))
output_box.pack(padx=20, pady=2, expand=True, fill="both")

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)

original_text_frame.grid_columnconfigure(0, weight=1)
original_text_frame.grid_columnconfigure(1, weight=1)
original_text_frame.grid_rowconfigure(0, weight=15)
original_text_frame.grid_rowconfigure(1, weight=1)

root.mainloop()
