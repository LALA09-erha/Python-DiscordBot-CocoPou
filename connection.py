import mysql.connector
import instaloader
import api as a
import pymongo



# Create a new client and connect to the server



def connect():
  global mydb
  uri = "mongodb+srv://lalaerha:bp8GlR3fWrH7lL59@cluster0.yyqsrnb.mongodb.net/?retryWrites=true&w=majority"
  try:
    clnt = pymongo.MongoClient(uri)
    mydb = clnt['dc_db']
    
  except:
    return False


# insert data to database
def insert_yt(data):
  cur = mydb['yt']
  cur.insert_one(data)
  return True


# update live link
def checkupdate_ytlive(link, id):
  cur = mydb['yt']
  cur.update_one({"_id": id}, {"$set": {"link_live": link}})
  return True



# update short link
def checkupdate_ytsr(link, id):
  cur = mydb['yt']
  cur.update_one({"_id": id}, {"$set": {"link_short": link}})
  return True
  


# check update checkupdate_yt
def checkupdate_yt(link, id):
  cur = mydb['yt']
  cur.update_one({"_id": id}, {"$set": {"link": link}})
  return True
  


# get all data yt
def getdata_yt():
  cur = mydb['yt']
  data = cur.find()
  return list(data)
  


# cek username in database (tidak boleh ada channel yang sama dalam satu server)
def cekusername_yt(username, server):
  cur = mydb['yt']
  data = cur.find({"username": username, "server_id": server})
  if len(list(data)) == 0:
    return True
  else:
    return False


# cek max limit
def cekmax_yt(server):
  cur = mydb['yt']
  data = cur.find({"server_id": server})
  if len(list(data)) < 3:
    return True
  else:
    return False


# delete user yt
def delete_yt(username, server):
  cur = mydb['yt']
  cur.delete_one({"username": username, "server_id": server})
  return True



# check data berita in database
def check_berita(data):
  cur = mydb['berita']
  data = cur.find({"bola": data['bola'], "server_id": data['server_id'], "channel_id": data['channel_id']})
  if len(list(data)) == 0:
    return True
  else:
    return False


# insert berita to database
def insert_berita(data):
  cur = mydb['berita']
  check = check_berita(data)
  
  if check == False:
    return False
  else:
    cur.insert_one(data)
    return True


# get all data berita in database
def getdata_berita():
  cur = mydb['berita']
  data = cur.find()
  return list(data)

# delete berita
def delete_berita(server):
  cur = mydb['berita']
  cur.delete_one({"server_id": server})
  return True

# update tanggal berita
def update_berita(id, tanggal):
  cur = mydb['berita']
  cur.update_one({"_id": id}, {"$set": {"tanggal": tanggal}})
  return True
