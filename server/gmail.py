def think_of_better_name(access_token):
    # Use the access token to query the Gmail API
    creds = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=creds)

    # Retrieve messages from the user's Gmail inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=25).execute()
    messages = results.get('messages', [])

    emails = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        parts = msg['payload'].get('parts', [])

        # Find the subject in the headers
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
        
        attachments = []
        for part in parts:
            filename = part.get('filename')
            mime_type = part.get('mimeType')
            body = part.get('body')
            
            if 'attachmentId' in body:
                attachment_id = body['attachmentId']
                attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachment_id).execute()


                data = attachment.get('data')
                
                if data:
                    # Decode the base64 encoded attachment data
                    data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    attachments.append({
                        'filename': filename,
                        'mimeType': mime_type,
                    })

        emails.append({
            'subject': subject,
            'attachments': attachments
        })