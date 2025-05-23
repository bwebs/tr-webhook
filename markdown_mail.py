from courier.client import Courier

# Initialize the Courier client
client = Courier()


def send_markdown_message(markdown_content: str, subject: str):
    """
    Send a message using a Courier template with markdown content.

    Args:
        markdown_content (str): The markdown content to be sent
    """
    try:
        response = client.send(
            message={
                "template": "8XBK02CCQ3MFFRQA91CZRYRRYF7K",
                "to": [
                    {"email": "bryanweber@google.com"},
                    {"email": "marold@google.com"},
                ],
                "data": {"markdown": markdown_content, "subject": subject},
            }
        )
        return response
    except Exception as e:
        print(f"Error sending message: {e}")
        raise
