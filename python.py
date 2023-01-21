import html
from flask import Flask,render_template, render_template_string,url_for,request,redirect,session
import mysql.connector
import mariadb
from werkzeug.security import generate_password_hash,check_password_hash

#baza podataka
konekcija = mysql.connector.connect(
 passwd="", # lozinka za bazu
 user="root", # korisničko ime
 database="ace2", # ime baze
 port=3306, # port na kojem je mysql server
 auth_plugin='mysql_native_password' # ako se koristi mysql 8.x
)
kursor = konekcija.cursor(dictionary=True)



##fighter##
app=Flask(__name__)
app.secret_key="tajni_kljuc_aplikacije"


@app.route('/',methods=['GET','POST'])
def home():
    return render_template('login.html')
#login u pokusaju
@app.route('/login',methods=['GET','POST'])
def render_login():
    if request.method=="GET":
        return render_template('login.html')

    if request.method=="POST":
        forma=request.form
        upit="SELECT * FROM fighter where email=%s"
        vrednost=(forma["email"],)
        kursor.execute(upit,vrednost)
        fighter=kursor.fetchone()
        if check_password_hash(fighter["password"],forma["password"]):
            session["ulogovani_fighter"]=str(fighter)
            return redirect(url_for("fighter"))

        else:
            return render_template("login.html")
    
#login u pokusaju




#logout
@app.route("/logout")
def logout():
    session.pop("ulogovani_fighter",None)
    return redirect(url_for("render_login"))

#globalna funkcija ulogovan()
def ulogovan():
    if "ulogovani_fighter" in session:
        return True
    else:
        return False

##dodaj fighter##
@app.route('/fighter',methods=['GET','POST']) ##
def render_fighter():
    upit="select * from fighter"
    kursor.execute(upit)
    fighter=kursor.fetchall()
    return render_template('fighter.html',fighter=fighter)

@app.route('/novi',methods=['GET','POST'])
def render_novi():
    if request.method=="GET":
        return render_template('fighter_novi.html')

    if request.method=="POST":
        forma=request.form
        hesovana_lozinka=generate_password_hash(forma["password"])
        vrednosti=(
            forma["ime"],
            forma["prezime"],
            forma["email"],
            forma["godina"],
            forma["kategorija"],
            forma["rola"],
            hesovana_lozinka
        )
    upit="""insert into
               fighter(ime,prezime,email,godina,kategorija,rola,password)
               values(%s,%s,%s,%s,%s,%s,%s)
    """
    kursor.execute(upit,vrednosti)
    konekcija.commit()
    return redirect(url_for("render_fighter"))

##brisi fighter##
@app.route('/brisi/<id>',methods=["POST"])
def fighter_brisanje(id):
    upit="""
    DELETE FROM fighter WHERE id=%s
    """
    vrednost=(id,)
    kursor.execute(upit,vrednost)
    konekcija.commit()
    return redirect(url_for("render_fighter"))

##menjaj fighter
@app.route('/izmena/<id>',methods=['GET','POST'])
def render_izmena(id):
    if request.method=="GET":
        upit="select * from fighter where id=%s"
        vrednost=(id,)
        kursor.execute(upit,vrednost)
        fighter=kursor.fetchone()
        return render_template("fighter_izmena.html",fighter=fighter)
    
    if request.method=="POST":
        upit="""update fighter set
                 ime=%s,prezime=%s,email=%s,password=%s,godina=%s,kategorija=%s,rola=%s
                 where id=%s
        """
        forma=request.form
        vrednost=(
            forma["ime"],
            forma["prezime"],
            forma["email"],
            forma["password"],
            forma["godina"],
            forma["kategorija"],
            forma["rola"],
            id,
        )
        kursor.execute(upit,vrednost)
        konekcija.commit()
        return redirect(url_for('render_fighter'))



##promoter##
@app.route('/promoter',methods=['GET'])
def render_promoter():
    upit="select * from promoter"
    kursor.execute(upit)
    promoter=kursor.fetchall()
    return render_template('promoter.html',promoter=promoter)
##dodaj promotera

@app.route('/addpromoter',methods=['GET','POST'])
def render_addpromoter():
    if request.method=="GET":
        return render_template('promoter_novi.html')

    if request.method=="POST":
        forma=request.form
        vrednost=(
            forma["ime"],
            forma["prezime"],
            forma["email"],
            forma["godina"],
            forma["rola"]
        )
        upit="""insert into
                  promoter(ime,prezime,email,godina,rola)
                  values(%s,%s,%s,%s,%s)
        """
        kursor.execute(upit,vrednost)
        konekcija.commit()
        return redirect(url_for("render_promoter"))


##izmeni promotera
@app.route('/izmena1/<id>',methods=['GET','POST'])
def render_izmena1(id):
    if request.method=="GET":
        upit="select * from promoter where id=%s"
        vrednost=(id,)
        kursor.execute(upit,vrednost)
        promoter=kursor.fetchone()
        return render_template("promoter_izmena.html",promoter=promoter)

    if request.method=="POST":
        upit="""update promoter set
                 ime=%s,prezime=%s,email=%s,godina=%s,rola=%s 
                 where id=%s   
        """
        forma=request.form
        vrednost=(
            forma["ime"],
            forma["prezime"],
            forma["email"],
            forma["godina"],
            forma["rola"],
            id,
        )
        kursor.execute(upit,vrednost)
        konekcija.commit()
        return redirect(url_for('render_promoter'))


##obrisi promotera
@app.route('/promoter_brisanje/<id>',methods=["POST"])
def promoter_brisanje(id):
    upit="""
    DELETE FROM promoter where id=%s
    """
    vrednost=(id,)
    kursor.execute(upit,vrednost)
    konekcija.commit()
    return redirect(url_for("render_promoter"))



##promocija prikaz iz tabele
@app.route('/promo',methods=['GET'])
def render_promocija():
    upit="select * from promocija"
    kursor.execute(upit)
    promocija=kursor.fetchall()
    return render_template('promocija.html',promocija=promocija)
##kreiranje nove promocije
@app.route('/novi2',methods=['GET','POST'])
def render_addpromo():
    if request.method=="GET":
        return render_template('promocija_novi.html')

    if request.method=="POST":
        forma=request.form
        vrednosti=(
            forma["name"],
            forma["godina"],
            forma["sport"],
            forma["boss"]
        )
        upit="""insert into
                  promocija(name,godina,sport,boss)
                  values(%s,%s,%s,%s)
        """
        kursor.execute(upit,vrednosti)
        konekcija.commit()
        return redirect(url_for("render_promocija"))


##brisanje promocije
@app.route("/promocija_brisanje/<id>",methods=["POST"])
def promocija_brisanje(id):
    upit="""
    DELETE FROM promocija WHERE id=%s
    """
    vrednost=(id,)
    kursor.execute(upit,vrednost)
    konekcija.commit()
    return redirect(url_for("render_promocija"))


##izmena promocije
@app.route('/izmena2/<id>',methods=['GET','POST'])
def render_izmena2(id):
    if request.method=="GET":
        upit="select * from promocija where id=%s"
        vrednost=(id,)
        kursor.execute(upit,vrednost)
        promocija=kursor.fetchone()
        return render_template("promocija_izmena.html",promocija=promocija)

    if request.method=="POST":
        upit="""update promocija set
                 name=%s,godina=%s,sport=%s,boss=%s
                 where id=%s
        """
        forma=request.form
        vrednost=(
            forma["name"],
            forma["godina"],
            forma["sport"],
            forma["boss"],
            id,
        )
        kursor.execute(upit,vrednost)
        konekcija.commit()
        return redirect(url_for('render_promocija'))



app.run(debug=True)


