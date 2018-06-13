
import tweepy
import pymysql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import schedule
import time


msg = MIMEMultipart()
msg['from'] = "elexamenmasrudo@gmail.com"
msg['To'] = "rojo@itcr.ac.cr"
msg['Subject'] = 'Tweets Equipo Jeannette Keylor Bryan'
password = "JKBredes2018"

def enviarCorreo(cuerpoCorreo):

    body = cuerpoCorreo
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(msg['from'], password)
    server.sendmail(msg['from'], msg['To'], msg.as_string())
    server.quit()

def twiter():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='twitter', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    #cursor = connection.cursor()

    consumer_key = '544Oo6cZxWAMBxLkSS65fCVjP'
    consumer_secret = '6CkCohOoYZrRRflbqSz4YUvHDUGcT86kDwZS1jS4M88E92yuxk'

    access_token = '891444092-HipG3Dp8hJo3MK5WpnxTX4vqs6eLqjTcYTNyxf7H'
    access_token_secret = '0Yp6bMIcw30vIgYLr2wyYue5nYh2YIJf0PEACQiW9i5DA'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    listaTweetsT = []
    listaTweetE = []
    cont = 0

    # Buscar tweets
    public_tweets = api.search(q ='#intentadoSalvarElSemestreConRojo', count=100)


    with connection.cursor() as cursor:
        try:
            for tweet in public_tweets:
                print(tweet.created_at, tweet.author.screen_name)
                add = ("INSERT INTO `tweet` (`hora`, `usuario`, `cuerpo`) VALUES (%s, %s, %s)")
                cursor.execute(add, (tweet.created_at, tweet.author.screen_name, tweet.text))
                connection.commit()
                listaTweetsT.append(tweet.text)
            cantEnvios = len(listaTweetsT)
            print("entrando")
            con=10
            lista_valores_1 = []
            while(con>0):
                print("Entra al while")
                rand = random.randint(0,cantEnvios)
                lista_valores_1.append(listaTweetsT[rand])
                con-=1
            print("Sale del ciclo")

            enviarCorreo(str(lista_valores_1))

        finally:
            connection.close()

schedule.every().hour.do(twiter)
twiter()