import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import csv

class SearchApp(App):
	def build(self):
		self.layout = BoxLayout(orientation='vertical')
		self.search_field = TextInput(hint_text='Enter phone number')
		self.exact_match_label_shadow = Label(size_hint_y=None, halign="center", valign="middle", color=[0, 0, 0, 0.5])  # Shadow label for exact matches
		self.exact_match_label = Label(size_hint_y=None, halign="center", valign="middle", bold=True, color=[1, 1, 1, 1])  # New label for exact matches
		self.result_label = Label(size_hint_y=None, halign="center")  # Allow vertical resizing of label
		self.exact_match_label_shadow.bind(width=lambda *x: self.exact_match_label_shadow.setter('text_size')(self.exact_match_label_shadow, (self.exact_match_label_shadow.width, None)), height=lambda *x: self.exact_match_label_shadow.setter('text_size')(self.exact_match_label_shadow, (None, self.exact_match_label_shadow.height)))
		self.exact_match_label.bind(width=lambda *x: self.exact_match_label.setter('text_size')(self.exact_match_label, (self.exact_match_label.width, None)), height=lambda *x: self.exact_match_label.setter('text_size')(self.exact_match_label, (None, self.exact_match_label.height)))
		self.result_label.bind(width=lambda *x: self.result_label.setter('text_size')(self.result_label, (self.result_label.width, None)), texture_size=lambda *x: self.result_label.setter('height')(self.result_label, self.result_label.texture_size[1]))
		self.layout_exact = BoxLayout(orientation='vertical')  # New layout for exact matches
		self.scroll_view_exact = ScrollView()  # Create a ScrollView for exact matches
		self.scroll_view_exact.add_widget(self.layout_exact)  # Add the layout to the ScrollView
		self.layout_exact.add_widget(self.exact_match_label_shadow)  # Add the shadow label to the layout
		self.layout_exact.add_widget(self.exact_match_label)  # Add the exact match label to the layout
		self.scroll_view_partial = ScrollView()  # Create a ScrollView for partial matches
		self.scroll_view_partial.add_widget(self.result_label)  # Add the result label to the ScrollView
		self.email_button = Button(text='Email', on_press=self.send_email)
		self.layout.add_widget(self.search_field)
		self.layout.add_widget(self.scroll_view_exact)  # Add the ScrollView for exact matches to the layout
		self.layout.add_widget(self.scroll_view_partial)  # Add the ScrollView for partial matches to the layout
		self.layout.add_widget(self.email_button)
		return self.layout

	def on_start(self):
		self.search_field.bind(text=self.search_csv)

	def search_csv(self, instance, value):
		if value:  # Only attempt to search if value is not empty
			with open('numbers.csv', 'r') as f:
				reader = csv.reader(f)
				exact_match = []
				partial_matches = []
				for row in reader:
					if row and value == row[0]:  # Check that row is not empty and is an exact match
						exact_match.append(', '.join(row))
					elif row:  # Check that row is not empty
						for cell in row:  # Check each cell in the row
							if value in cell:  # If the search value is in the cell
								partial_matches.append(', '.join(row))
								break  # No need to check the rest of the cells in this row
				self.exact_match_label_shadow.text = '\n'.join(exact_match)
				self.exact_match_label.text = '\n'.join(exact_match)
				self.result_label.text = '\n'.join(partial_matches)                

	def send_email(self, instance):
		# Extract email from result label
		receiver_address = self.exact_match_label.text.split(',')[-2].strip() if ',' in self.exact_match_label.text else None

		# Only attempt to send an email if a valid email address is present
		if receiver_address:
			# The mail addresses and password
			sender_address = 'sender@gmail.com'
			sender_pass = 'password'
			
			# Setup the MIME
			message = MIMEMultipart()
			message['From'] = sender_address
			message['To'] = receiver_address
			message['Subject'] = 'A test mail sent by Python. It has an attachment.'   # The subject line
			
			# The body and the attachments for the mail
			mail_content = f"Customer with phone number {self.search_field.text} is having issues."
			message.attach(MIMEText(mail_content, 'plain'))
			
			# Create SMTP session for sending the mail
			session = smtplib.SMTP('smtp.gmail.com', 587)  # Use gmail with port
			session.starttls()  # Enable security
			session.login(sender_address, sender_pass)  # Login with mail_id and password
			
			text = message.as_string()
			session.sendmail(sender_address, receiver_address, text)
			session.quit()

if __name__ == '__main__':
	SearchApp().run()
