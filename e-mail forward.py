import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Configure as credenciais da API do Gmail
credentials = Credentials.from_authorized_user_file('credentials.json')
service = build('gmail', 'v1', credentials=credentials)

# Defina o endereço de email de encaminhamento
forward_email = 'nf@bulbe.com.br'

# Função para verificar se o email contém anexos de notas fiscais
def has_invoice_attachments(message):
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if 'filename' in part:
                filename = part['filename']
                if filename.lower().endswith('.xml'):
                    return True
    return False

# Obtém a lista de emails não lidos
response = service.users().messages().list(userId='me', q='is:unread').execute()
messages = response.get('messages', [])

# Percorre os emails não lidos
for message in messages:
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    
    # Verifica se o email contém anexos de notas fiscais
    if has_invoice_attachments(msg):
        # Encaminha o email para o endereço especificado
        service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
        service.users().messages().send(userId='me', body={'raw': msg['raw'], 'forwardingEmail': forward_email}).execute()
