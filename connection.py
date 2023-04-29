
import mysql.connector
import instaloader
import api as a
bot = instaloader.Instaloader()

def connect():
    global mydb
    try:
        mydb = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12614298",
            password="",
            database = "sql12614298"
            )
        print(mydb)
    except:
        return False

# insert data to database
def insert_yt(data):
    cur = mydb.cursor()
    cur.execute(f"INSERT INTO tw (username, link, server_id, channel_id) VALUES ('{data['username']}', '{data['link']}', '{data['server_id']}', '{data['channel_id']}')")
    mydb.commit()
    return True

# update live link
def checkupdate_ytlive(link,id):
    cur = mydb.cursor()
    cur.execute(f"UPDATE tw SET link_live = '{link}' WHERE id_tw = '{id}'")
    mydb.commit()
    return True
# update short link 
def checkupdate_ytsr(link,id):
    cur = mydb.cursor()
    cur.execute(f"UPDATE tw SET link_short = '{link}' WHERE id_tw = '{id}'")
    mydb.commit()
    return True

# check update checkupdate_yt
def checkupdate_yt(link,id):
    cur = mydb.cursor()
    cur.execute(f"UPDATE tw SET link = '{link}' WHERE id_tw = '{id}'")
    mydb.commit()
    return True

# get all data yt
def getdata_yt():
    cur = mydb.cursor()
    cur.execute("select * from tw")
    data = cur.fetchall()
    return data

# cek username in database (tidak boleh ada channel yang sama dalam satu server)
def cekusername_yt(username,server):
    cur = mydb.cursor()
    cur.execute(f"select * from tw where username = '{username}' and server_id = '{server}'")
    data = cur.fetchall()
    if len(data) == 0:
        return True
    else:
        return False
    
# cek max limit
def cekmax_yt(server):
    cur = mydb.cursor()
    cur.execute(f"select * from tw where server_id = '{server}'")
    data = cur.fetchall()
    if len(data) < 3:
        return True
    else:
        return False
    
# delete user yt
def delete_yt(username,server):
    cur = mydb.cursor()
    cur.execute(f"delete from tw where username = '{username}' and server_id = '{server}'")
    mydb.commit()
    return True    

# check data berita in database
def check_berita(data):
    cur = mydb.cursor()
    cur.execute(f"select * from berita where bola = '{data['bola']}' and server_id = '{data['server_id']}' and channel_id = '{data['channel_id']}'")
    data = cur.fetchall()
    if len(data) == 0:
        return True
    else:
        return False

# insert berita to database
def insert_berita(data):
    cur = mydb.cursor()
    check = check_berita(data)
    if check == False:
        return False
    else:
        cur.execute(f"INSERT INTO berita (bola, server_id, channel_id,tanggal) VALUES ('{data['bola']}', '{data['server_id']}', '{data['channel_id']}' , '{data['tanggal']}')")
        mydb.commit()
        return True
    
# get all data berita in database
def getdata_berita():
    cur = mydb.cursor()
    cur.execute("select * from berita")
    data = cur.fetchall()
    return data

# delete berita
def delete_berita(server):
    cur = mydb.cursor()
    cur.execute(f"delete from berita where server_id = '{server}'")
    mydb.commit()
    return True

# update tanggal berita
def update_berita(id,tanggal):
    cur = mydb.cursor()
    cur.execute(f"UPDATE berita SET tanggal = '{tanggal}' WHERE id_berita = '{id}'")
    mydb.commit()
    return True