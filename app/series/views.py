from hashlib import new
from typing import List
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from app.models import Episode, Season, Serie, User, Commentary
from app.forms import EditSerie, RegisterEpisode, RegisterSeason, RegisterSerie, RegisterCommentary
from app import db

from . import series

@series.route('/series/new', methods=['GET', 'POST'])
@login_required
def register_serie():
    form = RegisterSerie()

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user:
            new_serie = Serie(form.serie_name.data, form.serie_type.data, user.id)
            db.session.add(new_serie)
            db.session.commit()
            return redirect(url_for('series.get_series_by_user'))
        
        flash("Erro ao cadastrar série. Tente novamente.", category="warning")
        return redirect(url_for('series.register_serie'))

    return render_template('register_serie.html', form=form)

@series.route('/series', methods=['GET'])
@login_required
def get_series_by_user():
    user = User.query.filter_by(id=current_user.get_id()).first()
    series = db.session.execute(f'SELECT * FROM Serie s WHERE s.user_id = {user.id}')
    return render_template('list_series.html', series=series)

@series.route('/series/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_serie(id):
    serie = Serie.query.get(int(id))
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user and serie:
            serie.name = request.form['serie_name']
            serie.user_id = user.id
            serie.serie_type = request.form['serie_type']
            db.session.commit()
            return redirect(url_for('series.get_series_by_user'))
        flash("Erro ao editar série. Tente novamente.", category="warning")
        return redirect(url_for('series.edit_serie'))
    return render_template('edit_serie.html', serie=serie)

@series.route('/series/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_serie(id):
    serie = Serie.query.get(int(id))
    if serie:
        db.session.delete(serie)
        db.session.commit()
        return redirect(url_for('series.get_series_by_user'))
    else:
        flash("Erro ao editar série. Tente novamente.", category="warning")
        return redirect(url_for('series.get_series_by_user'))

@series.route('/series/view/<id>', methods=['GET', 'POST'])
@login_required
def details_serie(id):
    form = RegisterCommentary()
    serie = Serie.query.get(int(id))
    seasons = db.session.execute(f'SELECT * FROM season s WHERE s.serie_id = {serie.id}')
    commentarys = db.session.execute(f'SELECT * FROM commentary c WHERE c.serie_id = {serie.id}')
    if seasons and commentarys:
        return render_template('details_serie.html', seasons=seasons, serie=serie, commentarys=commentarys, form=form)
    else:    
        flash("Erro ao encontrar série. Tente novamente.", category="warning")
        return redirect(url_for('series.get_series_by_user'))

@series.route('/series/<id>/commentary/new', methods=['GET', 'POST'])
@login_required
def add_commentary(id):
    serie = Serie.query.get(int(id))
    form = RegisterCommentary()
    if form.validate_on_submit():
        if serie:
            new_commentary = Commentary(text = form.commentary_text.data, serie_id=serie.id)
            db.session.add(new_commentary)
            db.session.commit()
            return redirect(url_for('series.details_serie', id=id))
    return redirect(url_for('series.details_serie', id=id))

@series.route('/series/<serie_id>/commentary/delete/<commentary_id>', methods=['GET', 'POST'])
@login_required
def delete_commentary(serie_id,commentary_id):
    serie = Serie.query.get(int(serie_id))
    commentary = Commentary.query.get(int(commentary_id))
    if serie and commentary:
        db.session.delete(commentary)
        db.session.commit()
        return redirect(url_for('series.details_serie', id=serie_id))
    else:
        flash("Erro ao deletar comentário. Tente novamente.", category="warning")
        return redirect(url_for('series.details_serie', id=serie_id))

@series.route('/series/<id>/seasons/add', methods=['GET', 'POST'])
@login_required
def add_seasons(id):
    form = RegisterSeason()
    serie = Serie.query.get(int(id))
    count = 0
    if request.method == "GET":
        if serie:
            return render_template('add_seasons.html', serie=serie, form=form, count=count)
    if request.method == "POST":
        seasons_number = form.seasons_number.data
        list_season = []
        while(count < seasons_number):
            season = Season(count + 1, serie.id)
            list_season.append(season)
            count += 1
        db.session.add_all(list_season)
        serie.seasons = list_season
        db.session.commit()
        return redirect(url_for('series.details_serie', id=id))

@series.route('/serie/<serie_id>/seasons/view/<season_id>', methods=['GET'])
@login_required
def detail_season(serie_id, season_id):
    serie = Serie.query.get(int(serie_id))
    season = Season.query.get(int(season_id))
    episodes = db.session.execute(f'SELECT * FROM episode e WHERE e.season_id = {season.id}')
    return render_template('details_season.html', serie=serie, season=season, episodes=episodes)

@series.route('/series/<serie_id>/seasons/<season_id>', methods=['GET', 'POST'])
@login_required
def edit_season(serie_id, season_id):
    form = RegisterEpisode()
    serie = Serie.query.get(int(serie_id))
    season = Season.query.get(int(season_id))
    count = 0
    if request.method == "GET":
        if season:
            return render_template('edit_seasons.html', season=season, form=form)
    if request.method == "POST":
        episodes_number = form.episodes_number.data
        list_episodes = []
        while(count < episodes_number):
            episode = Episode(count + 1, season.id)
            list_episodes.append(episode)
            count += 1
        db.session.add_all(list_episodes)
        season.episodes = list_episodes
        db.session.commit()
        return redirect(url_for('serie.details_season', id=id))
        
    