def is_significant_change(old_text, new_text):

    old = old_text.strip()
    new = new_text.strip()

    return old != new


def send_notification(document_id):

    print(f"Significant change detected in document {document_id}")