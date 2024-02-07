import sqlite3
from flask import Flask, redirect, render_template, request, url_for


app=Flask(__name__)




data=[]
def veriAl():
    global data
    with sqlite3.connect('list.db') as con:
        cur=con.cursor()
        cur.execute("select*from tblList")
        data=cur.fetchall()
        for i in data:
            print(i)



def veriEkle(name,artist,year,typ,time):
    with sqlite3.connect('list.db') as con:
        cur=con.cursor()
        cur.execute("insert into tblList(musicName, musicArtist, musicYear, musicTyp, musicTime) values(?,?,?,?,?)", (name, artist, year, typ, time))
        con.commit()
        print("veriler eklendi")


def veriSil(id):
    with sqlite3.connect('list.db') as con:
        cur = con.cursor()
        cur.execute("delete from tblList where id=?", (id,))
        con.commit()
    print("veriler silindi")


def veriGuncelle(id,name,artist,year,typ,time):
    with sqlite3.connect('list.db') as con:
        cur=con.cursor()
        cur.execute("update tblList set musicName=?, musicArtist=?, musicYear=?, musicTyp=?, musicTime=? where id=?", (name, artist, year, typ, time, id))

        con.commit()
        print("veriler guncellendi")










@app.route("/index")
def index():
    music=[
        {
            'musicName':'Affet' 
        },
        {
            'musicName':'my life'
        }
    ]


    return render_template("index.html",musics=music)



@app.route("/liste")
def liste():

  
    veriAl()

    return render_template("liste.html",veri=data)



@app.route("/hakkımda")
def hakkımda():


    return render_template("hakkımda.html")


@app.route("/muzikekle",methods=['GET','POST'])
def muzikekle():
    print("muzikekle")
    if request.method == "POST":
       musicName=request.form['musicname']
       musicArtist=request.form['musicartist']
       musicYear=request.form['musicyear']
       musicTyp=request.form['musictyp']
       musicTime=request.form['musictime']
       veriEkle(musicName, musicArtist, musicYear,musicTyp, musicTime)
     
    return render_template("muzikekle.html")



@app.route("/muziksil/<string:id>")
def muziksil(id):
    print("muziksil silinecek id",id)
    veriSil(id)
    return redirect(url_for("liste"))

@app.route("/muzikguncelle/<string:id>",methods=['GET','POST'])
def muzikguncelle(id):
    if request.method=='GET':

     print("guncellenecek id",id)
     guncellenecekVeri=[]
     for d in data:
        if str(d[0]) == id:
            guncellenecekVeri = list(d)
     return render_template("muzikguncelle.html",veri=guncellenecekVeri)
        
    else:
       musicID=request.form['musicID']
       musicName=request.form['musicname']
       musicArtist=request.form['musicartist']
       musicYear=request.form['musicyear']
       musicTyp=request.form['musictyp']
       musicTime=request.form['musictime']
    veriGuncelle(musicID,musicName, musicArtist, musicYear,musicTyp, musicTime)
    return redirect(url_for("liste"))





@app.route("/muzikdetay/<string:id>")
def muzikdetay(id):
    detayVeri=[]
    for d in data:
     if str(d[0]) == id:
      detayVeri = list(d)
    return render_template("muzikdetay.html",veri=detayVeri)
        
 






 
if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8080)



