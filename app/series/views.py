from flask import render_template, redirect, flash, session, url_for, request
from flask_login import login_required, current_user
from app.models import Episode, Season, Serie, User, Commentary
from app.forms import RegisterEpisode, RegisterSeason, RegisterSerie, RegisterCommentary, EditEpisode, QuerySeries

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
    query_form = QuerySeries()
    user = User.query.filter_by(id=current_user.get_id()).first()
    series = db.session.execute(f'SELECT * FROM Serie s WHERE s.user_id = {user.id}')
    private = db.session.execute(f'SELECT private FROM public."user" s WHERE s.id = {user.id}').first()
    genders = db.session.execute(f'SELECT DISTINCT serie_type FROM Serie s WHERE s.user_id = {user.id}')
    query_form.gender.choices = [("")]+[g.serie_type for g in genders] 
    return render_template('list_series.html', series=series, private=private, query_form=query_form)

@series.route('/series/privar', methods=['GET'])
@login_required
def private_user_profile():
    user = User.query.filter_by(id=current_user.get_id()).first()
    user.private = True
    db.session.commit()
    return redirect(url_for('series.get_series_by_user'))

@series.route('/series/desprivar', methods=['GET'])
@login_required
def unprivate_user_profile():
    user = User.query.filter_by(id=current_user.get_id()).first()
    user.private = False
    db.session.commit()
    return redirect(url_for('series.get_series_by_user'))

@series.route('/query_series', methods=['GET','POST'])
@login_required
def get_series_by_user_query():
    query_form = QuerySeries()
    user = User.query.filter_by(id=current_user.get_id()).first()
    genders = db.session.execute(f'SELECT DISTINCT serie_type FROM Serie s WHERE s.user_id = {user.id}')
    query_form.gender.choices = [("")]+[g.serie_type for g in genders] 
    if query_form.validate_on_submit():
        if query_form.gender.data == "":
            series = db.session.execute(f"SELECT * FROM Serie s WHERE s.name LIKE '%{query_form.search_value.data}%' AND s.user_id = {user.id}")
        else:
            series = db.session.execute(f"SELECT * FROM Serie s WHERE s.name LIKE '%{query_form.search_value.data}%' AND s.serie_type = '{query_form.gender.data}' AND s.user_id = {user.id}")
        private = db.session.execute(f'SELECT private FROM public."user" s WHERE s.id = {user.id}').first()
        return render_template('list_series.html', series=series, private=private, query_form=query_form)
    else:
        return redirect(url_for('series.get_series_by_user'))



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
    seasons = db.session.execute(f'SELECT * FROM season s WHERE s.serie_id = {serie.id} ORDER BY s.season_number')
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

@series.route('/serie/<serie_id>/seasons/<season_id>', methods=['GET', 'POST'])
@login_required
def delete_season(serie_id, season_id):
    season = Season.query.get(int(season_id))
    
    if season:
        db.session.delete(season)
        db.session.commit()

    return redirect(url_for('series.details_serie', id=serie_id))

@series.route('/serie/<serie_id>', methods=['GET', 'POST'])
@login_required
def add_single_season(serie_id):
    serie = Serie.query.get(int(serie_id))
    count = 1
    
    if serie:
        seasons = db.session.execute(f'SELECT * FROM season s WHERE s.serie_id = {serie.id}')
        if seasons:
            for season in seasons:
                count = count + 1

        new_season = Season(count, serie.id)
        db.session.add(new_season)
        serie.seasons.append(new_season)
        db.session.commit()

    return redirect(url_for('series.details_serie', id=serie_id))

@series.route('/serie/<serie_id>/seasons/view/<season_id>', methods=['GET'])
@login_required
def detail_season(serie_id, season_id):
    serie = Serie.query.get(int(serie_id))
    season = Season.query.get(int(season_id))
    episodes = db.session.execute(f'SELECT * FROM episode e WHERE e.season_id = {season.id} ORDER BY e.episode_number')
    return render_template('details_season.html', serie=serie, season=season, episodes=episodes)

@series.route('/series/<serie_id>/seasons/<season_id>', methods=['GET', 'POST'])
@login_required
def edit_season(serie_id, season_id):
    form = RegisterEpisode()
    serie = Serie.query.get(int(serie_id))
    season = Season.query.get(int(season_id))
    return render_template('edit_seasons.html', serie=serie, season=season, form=form)

@series.route('/seasons/<id>/add', methods=['GET', 'POST'])
@login_required
def add_episodes(id):
    form = RegisterEpisode()
    season = Season.query.get(int(id))
    serie= Serie.query.get(int(season.serie_id))
    count = 0
    if request.method == "GET":
        if season:
            return render_template('add_episodes.html', season=season, serie=serie, form=form, count=count)
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
        return redirect(url_for('series.detail_season', serie_id=season.serie_id, season_id=season.id))

@series.route('/season/<season_id>', methods=['GET', 'POST'])
@login_required
def add_single_episode(season_id):
    season = Season.query.get(int(season_id))
    count = 1
    
    if season:
        episodes = db.session.execute(f'SELECT * FROM episode e WHERE e.season_id = {season.id}')
        if episodes:
            for episode in episodes:
                count = count + 1

        new_episode = Episode(count, season.id)
        db.session.add(new_episode)
        season.episodes.append(new_episode)
        db.session.commit()

    return redirect(url_for('series.detail_season', serie_id=season.serie_id, season_id=season.id))

@series.route('/episode/<id>', methods=['GET', 'POST'])
@login_required
def edit_episode(id):
    episode = Episode.query.get(int(id))
    season = Season.query.get(int(episode.season_id))
    serie = Serie.query.get(int(season.serie_id))
    if episode.concluded:
        episode.concluded = False
    else:
        episode.concluded = True
    db.session.commit()
    season_episodes = season.episodes
    count_episode = len(season_episodes)
    verifier_episode = 0
    for season_episode in season_episodes:
        if season_episode.concluded == True:
            verifier_episode += 1
    if verifier_episode == count_episode:
        season.concluded = True
    else:
        season.concluded = False
    serie_seasons = serie.seasons
    count_season = len(serie_seasons)
    verifier_season = 0
    for serie_season in serie_seasons:
        if serie_season.concluded == True:
            verifier_season += 1
    if verifier_season == count_season:
        serie.concluded = True
    else:
        serie.concluded = False
    db.session.commit()
    return redirect(url_for('series.detail_season', serie_id=season.serie_id, season_id=season.id))

@series.route('/episode/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_episode(id):
    episode = Episode.query.get(int(id))
    season = Season.query.get(int(episode.season_id))
    serie = Serie.query.get(int(season.serie_id))
    if episode and season and serie:
        db.session.delete(episode)
        db.session.commit()
        return redirect(url_for('series.detail_season', serie_id=serie.id, season_id=season.id))
    else:
        flash("Erro ao deletar episódio. Tente novamente.", category="warning")
        return redirect(url_for('series.detail_season', serie_id=serie.id, season_id=season.id))


@series.route('/series/publico/<id>', methods=['GET','POST'])
@login_required
def get_series_by_public_user(id):
    user = User.query.filter_by(id=id).first()
    query_form = QuerySeries()
    series = db.session.execute(f'SELECT * FROM Serie s WHERE s.user_id = {user.id}')
    genders = db.session.execute(f'SELECT DISTINCT serie_type FROM Serie s WHERE s.user_id = {user.id}')
    query_form.gender.choices = [("")]+[g.serie_type for g in genders] 
    return render_template('list_series_public.html', series=series, user=user, query_form=query_form)

@series.route('/series/publico/<id>/query_series', methods=['GET','POST'])
@login_required
def get_public_series_by_user_query(id):
    query_form = QuerySeries()
    user = User.query.filter_by(id=id).first()
    genders = db.session.execute(f'SELECT DISTINCT serie_type FROM Serie s WHERE s.user_id = {id}')
    query_form.gender.choices = [("")]+[g.serie_type for g in genders] 
    if query_form.validate_on_submit():
        if query_form.gender.data == "":
            series = db.session.execute(f"SELECT * FROM Serie s WHERE s.name LIKE '%{query_form.search_value.data}%' AND s.user_id = {id}")
        else:
            series = db.session.execute(f"SELECT * FROM Serie s WHERE s.name LIKE '%{query_form.search_value.data}%' AND s.serie_type = '{query_form.gender.data}' AND s.user_id = {id}")
        return render_template('list_series_public.html', user=user, series=series, query_form=query_form)
    else:
        return redirect(url_for('series.get_series_by_public_user',id=id))

@series.route('/series/view/public/<user_id>/<serie_id>', methods=['GET', 'POST'])
@login_required
def details_public_serie(user_id,serie_id):
    serie = Serie.query.get(int(serie_id))
    seasons = db.session.execute(f'SELECT * FROM season s WHERE s.serie_id = {serie.id}')
    commentarys = db.session.execute(f'SELECT * FROM commentary c WHERE c.serie_id = {serie.id}')
    if seasons and commentarys:
        return render_template('details_public_serie.html', user_id = user_id, serie=serie, seasons=seasons, commentarys=commentarys)
    else:    
        flash("Erro ao encontrar série. Tente novamente.", category="warning")
        return redirect(url_for('series.get_series_by_public_user',id=user_id))

@series.route('/serie/view/public/<user_id>/<serie_id>/<season_id>', methods=['GET'])
@login_required
def details_public_season(user_id,serie_id, season_id):
    serie = Serie.query.get(int(serie_id))
    season = Season.query.get(int(season_id))
    episodes = db.session.execute(f'SELECT * FROM episode e WHERE e.season_id = {season.id}')
    return render_template('details_public_season.html', user_id=user_id, serie=serie, season=season, episodes=episodes)