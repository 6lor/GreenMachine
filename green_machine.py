from tkinter import *
import tkinter as tk

import requests
import threading
import sys

from pytz import timezone
from functools import partial
from time import sleep
from json import loads
from datetime import datetime

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.text = "Instagram post ID"
		self.post_id = ""
		self.pack()
		self.create_widgets()
		self.color_bg = "#354d33"
		self.color_input = "#50704d"
		# If error 400 is present, replace hash query
		self.hash_query = "77fa889ea175f55eea62d9285abc769d"

	def create_widgets(self):

		self.responce = tk.Text(self)
		self.responce.configure(bg="#50704d", fg="white")
		self.responce.insert(INSERT, "Welcome to Green Machine v 1.0!")
		self.responce.grid(row=0, columnspan=2)

		self.text1 = tk.Label(self, text=self.text)
		self.text1.configure(bg="#354d33", fg="white")
		self.text1.grid(row=1, column=0)

		self.text2 = tk.Label(self, text="Frequency in seconds")
		self.text2.configure(bg="#354d33", fg="white")
		self.text2.grid(row=1, column=1)

		self.post_id_field = tk.Entry(self)
		self.post_id_field.configure(bg="#50704d", fg="white")
		self.post_id_field.grid(row=2, column=0)

		self.post_frequency = tk.Entry(self)
		self.post_frequency.configure(bg="#50704d", fg="white")
		self.post_frequency.insert(0,300)
		self.post_frequency.grid(row=2, column=1)

		self.set_post_id = tk.Button(self)
		self.set_post_id.configure(highlightbackground="#354d33", fg="black")
		self.set_post_id["text"] = "Set Post ID"
		self.set_post_id["command"] = lambda: self.set_value_for_post_id(self.post_id_field.get())
		self.set_post_id.grid(row=3, column=0, pady=(5,5))

		self.start_button = tk.Button(self)
		self.start_button.configure(highlightbackground="#354d33", fg="black")
		self.start_button["text"] = "Start!"
		self.start_button["command"] = self.runner_start
		self.start_button.grid(row=3, column=1, pady=(5,5))

		self.quit = tk.Button(self, text="QUIT", fg="gray", highlightbackground="Red",
							  command=sys.exit)
		self.quit.grid(row=4, columnspan=2, pady=(5,5))

	def set_value_for_post_id(self, new_post_id):
		self.responce.insert(END, f"\nPost ID is set to {new_post_id}")
		self.post_id = new_post_id

	def runner_start(self):
		if self.post_id != "":
			self.start_button["text"] = "Stop!"
			self.start_button["command"] = self.runner_stop

			self.runner_thread = threading.Thread(target=self.get_these_views, args=(self.post_id,), daemon=True)
			self.runner_flag = True
			self.runner_thread.start()
		else:
			self.responce.insert(END, f"\nSet the ID before starting!")

	def runner_stop(self):
		self.start_button["text"] = "Start!"
		self.start_button["command"] = self.runner_start
		self.runner_flag = False

	def self_keep_running(self, value):
		self.keep_running = value

	def get_these_views(self, post_id):
		self.responce.insert(END, f"\nSending request with ID {self.post_id}")
		while self.runner_flag:
			r = requests.get(f"https://www.instagram.com/graphql/query/?query_hash={self.hash_query}&variables=%7B%22shortcode%22%3A%22{post_id}%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D")
			print(r.status_code)
			if r.status_code == 200:
				try:
					data = loads(r.text)

					# change the time zome if not in eastern time
					self.text = f"{datetime.now(timezone('US/Eastern'))} - Views: {data['data']['shortcode_media']['video_view_count']} and Likes: {data['data']['shortcode_media']['edge_media_preview_like']['count']}"
				except TypeError:
					self.text = "Unable to find likes and views!"
			else:
				self.text = "Invalid server responce"
			self.responce.insert(END, f"\n{self.text}")
			print(f"Responce value is: {self.text}")
			sleep(int(self.post_frequency.get()))
		self.responce.insert(END, f"\nThe request runner has stopped")

if __name__ == "__main__":
	root = tk.Tk()
	root.title("Green Machine")
	app = Application(master=root)
	app.configure(bg="#354d33")
	app.mainloop()