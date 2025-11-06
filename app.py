from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Reads from .env file

app = Flask(__name__)

# Using SQLite for student simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rockbands-mm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'SECRET'

db = SQLAlchemy(app)

# ==========================
# DATABASE MODELS
# ==========================


class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
 
    memberships = db.relationship('Memberships', back_populates='band', lazy=True)
    band_albums = db.relationship('BandAlbums', back_populates='band', lazy=True)

    # Direct shortcuts for many-to-many relationships
    albums = db.relationship(
        'Albums',
        secondary='band_albums',
        back_populates='bands',
        viewonly=True
    )
    
    members = db.relationship(
        'Members',
        secondary='memberships',
        back_populates='bands',
        viewonly=True
    )


class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))

    memberships = db.relationship('Memberships', back_populates='member', lazy=True)

    # Direct many-to-many shortcut
    bands = db.relationship(
        'Bands',
        secondary='memberships',
        back_populates='members',
        viewonly=True
    )


class Memberships(db.Model):
    MembershipID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    MemberID = db.Column(db.Integer, db.ForeignKey('members.MemberID'), nullable=False)
    StartYear = db.Column(db.Integer)
    EndYear = db.Column(db.Integer)
    Role = db.Column(db.Text)

    band = db.relationship('Bands', back_populates='memberships')
    member = db.relationship('Members', back_populates='memberships')
    
    # FIXED: Removed incorrect band_albums and bands relationships that referenced Albums


class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)

    # FIXED: Added missing band_albums relationship
    band_albums = db.relationship('BandAlbums', back_populates='album', lazy=True)
    
    # FIXED: Added direct shortcut for many-to-many relationship
    bands = db.relationship(
        'Bands',
        secondary='band_albums',
        back_populates='albums',
        viewonly=True
    )


class BandAlbums(db.Model):
    __tablename__ = 'band_albums'
    id = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    AlbumID = db.Column(db.Integer, db.ForeignKey('albums.AlbumID'), nullable=False)

    band = db.relationship('Bands', back_populates='band_albums')
    album = db.relationship('Albums', back_populates='band_albums')

# ==========================
# ROUTES
# ==========================


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bands/add', methods=['GET', 'POST'])
def add_band():
    if request.method == 'POST':
        new_band = Bands(
            BandName=request.form['bandname'],
            FormedYear=request.form['formedyear'],
            HomeLocation=request.form['homelocation']
        )
        db.session.add(new_band)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_band.html')


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    bands = Bands.query.all()  # Students see querying with relationships
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form['membername'],
            MainPosition=request.form['mainposition']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html', bands=bands)


@app.route('/albums/add', methods=['GET', 'POST'])
def add_album():
    bands = Bands.query.all()
    if request.method == 'POST':
        # FIXED: Removed invalid BandID field from Albums
        new_album = Albums(
            AlbumTitle=request.form['albumtitle'],
            ReleaseYear=int(request.form['releaseyear'])
        )
        db.session.add(new_album)
        db.session.flush()  # FIXED: Get the AlbumID before committing
        
        # FIXED: Create the band-album association properly
        band_album = BandAlbums(
            BandID=int(request.form['bandid']),
            AlbumID=new_album.AlbumID
        )
        db.session.add(band_album)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_album.html', bands=bands)


@app.route('/bands/view')
def view_by_band():
    bands = Bands.query.all()
    return render_template('display_by_band.html', bands=bands)


@app.route('/bands/view/<int:id>')
def view_band(id):
    # Shows real database relationship querying
    band = Bands.query.get_or_404(id)
    return render_template('display_by_band.html', bands=[band])


@app.route('/memberships/add', methods=['GET', 'POST'])
def add_membership():
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        membership = Memberships(
            BandID=int(request.form.get('bandid')),
            MemberID=int(request.form.get('memberid')),
            Role=request.form.get('role'),
            StartYear=int(request.form.get('startyear')) if request.form.get('startyear') else None,
            EndYear=int(request.form.get('endyear')) if request.form.get('endyear') else None
        )
        db.session.add(membership)
        db.session.commit()
        flash('Membership assigned', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('add_membership.html', bands=bands, members=members)


@app.route('/memberships/edit/<int:id>', methods=['GET', 'POST'])
def edit_membership(id):
    membership = Memberships.query.get_or_404(id)
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        membership.BandID = request.form.get('bandid')
        membership.MemberID = request.form.get('memberid')
        membership.Role = request.form.get('role')
        membership.StartYear = request.form.get('startyear') or None
        membership.EndYear = request.form.get('endyear') or None
        db.session.commit()
        flash('Membership updated', 'success')
        return redirect(url_for('view_by_band'))

    return render_template('edit_membership.html', membership=membership, bands=bands, members=members)


@app.route('/memberships/delete/<int:id>')
def delete_membership(id):
    membership = Memberships.query.get_or_404(id)
    db.session.delete(membership)
    db.session.commit()
    flash('Membership removed', 'success')
    return redirect(url_for('view_by_band'))


# Create DB if not exists
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)