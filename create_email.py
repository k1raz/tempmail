from tempmail import EMail
import json
import os

class CreateMail:
    def __init__(self, address: str = None, filename: str = "emails.json") -> None:
        self.filename = filename
        self.emails_data = self.load_emails()  # Загружаем существующие данные из файла

        if address is None:
            self.email = EMail()
            self.wait_messages()
        else:
            self.email = EMail(address=address)
            self._read_messages()

    def load_emails(self):
        """Загружает данные из JSON файла, если он существует."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as infile:
                return json.load(infile)
        return []

    def _read_messages(self):
        inbox = self.email.get_inbox()
        messages = []

        for msg_info in inbox:
            messages.append({
                "subject": msg_info.subject,
                "body": msg_info.message.body
            })
            print(msg_info.subject, msg_info.message.body)

        self.save_messages(messages)

    def wait_messages(self):
        print(self.email.address)
        self.save_account()
        msg = self.email.wait_for_message()
        print(msg.html_body)
        self.save_messages([{
            "subject": "New message",
            "fromAddress": msg.from_addr,
            "body": msg.html_body
        }])

    def save_account(self):
        """Сохраняет новый адрес электронной почты в структуре данных."""
        email_entry = {
            "email": self.email.address,
            "messages": []
        }
        self.emails_data.append(email_entry)
        self.save_to_file()

    def save_messages(self, messages):
        """Сохраняет сообщения в соответствующем объекте электронной почты."""
        for entry in self.emails_data:
            if entry["email"] == self.email.address:
                entry["messages"].extend(messages)
                break
        self.save_to_file()

    def save_to_file(self):
        """Сохраняет всю структуру данных в JSON файл."""
        with open(self.filename, "w") as outfile:
            json.dump(self.emails_data, outfile, indent=4)