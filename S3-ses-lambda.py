from __future__ import print_function

import json
import urllib
import boto3

print('Loading function')

s3 = boto3.client('s3')
cliente = boto3.client('ses')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    fichero = '<a class="ulink" href="https://s3-eu-west-1.amazonaws.com/datoscomefruta/' + str(key) +'" target="_blank">'+str(key)+'</a>'
    print(fichero)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        contenidoPDF='PDF '+str(key)+' generado automaticamente: ' + fichero
        contenidoZIP='ZIP '+str(key)+' generado automaticamente: ' + fichero
        asuntoPDF='PDF ComeFruta: ' + str(key)
        asuntoZIP='ZIP ComeFruta: ' + str(key)
		
        cuerpo = contenidoPDF if 'pdf' in str(key) else contenidoZIP
        asunto = asuntoPDF if 'pdf' in str(key) else asuntoZIP
        
        response2 = cliente.send_email(
            Destination={
                'ToAddresses': [
					'example@email.com'
                ]
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': cuerpo,
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': 'This is the message body in text format.',
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': asunto,
                },
            },
            ReplyToAddresses=[
            ],
            Source='',
            SourceArn='',
        )

        #print(response2)
        
        return response['ContentType']
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
