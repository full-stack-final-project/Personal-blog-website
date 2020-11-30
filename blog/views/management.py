import os
from flask import Blueprint, render_template, send_from_directory
from flask_login import login_user, logout_user
from flask_login import login_required, current_user
from blog.forms import bio_form, article_form, category_form, work_form, project_form, skill_form, bio_form
from blog.extensions import db
from flask_ckeditor import upload_success, upload_fail

from blog.models import Article, Category, Comment, Bio, Skill, Project, Work_
from flask import render_template, flash, redirect, url_for
from flask import  request, current_app

manage_blueprint = Blueprint('management', __name__)

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

def safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_to_last_page(default = 'blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

@manage_blueprint.route('/article/manage')
@login_required
def manage_article():
    page = request.args.get('page', 1, type=int)
    onepage = Article.query.order_by(
        Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['MANAGE_ARTICLE_PER_PAGE'])
    onepage_articles = onepage.items
    return render_template('manage/manage_article.html', page=page, pagination=onepage, articles=onepage_articles)


@manage_blueprint.route('/article/<int:article_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_article(article_id):
    form = article_form()
    article = Article.query.get_or_404(article_id)
    if form.validate_on_submit():
        article.title = form.title.data 
        article.body = form.body.data 
        article.post = Category.query.get(form.category.data)
        db.session.commit()
        flash('Updated', 'success')
        return redirect(url_for('blog.display_article', article_id=article.id))
    form.title.data = article.title
    form.body.data = article.body
    form.category.data = article.category_id
    return render_template('manage/edit_article.html', form=form)

@manage_blueprint.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Deleted', 'success')
    return redirect_to_last_page()

@manage_blueprint.route('/category/manage')
@login_required
def manage_category():
    return render_template('manage/manage_categories.html')

@manage_blueprint.route('/bio/edit', methods=['POST', 'GET'])
@login_required
def edit_bio():
    form = bio_form()
    bio = Bio.query.first()
    if form.validate_on_submit():
        bio.name = form.name.data 
        bio.current_job =form.current_job.data     
        bio.intro = form.body.data
        db.session.commit()
        flash('Updated', 'success')
        return redirect(url_for('.manage_bio'))
    form.name.data = bio.name
    form.current_job.data = bio.current_job
    form.body.data = bio.intro
    return render_template('manage/edit_bio.html', form=form, title='Bio') 

@manage_blueprint.route('/bio/add', methods=['POST', 'GET'])
@login_required
def add_bio():
    form = bio_form()
    if form.validate_on_submit():
        bio.name = form.name.data 
        bio.current_job =form.current_job.dat 
        bio.intro = form.body.data
        db.session.commit()
        flash('Updated', 'success')
        return redirect_to_last_page()
    return render_template('manage/add_bio.html', form=form, title='Bio')

@manage_blueprint.route('/skill/<int:skill_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_skill(skill_id):
    form = skill_form()
    skill = Skill.query.get(skill_id)
    if form.validate_on_submit():
        skill.content = form.content.data    
        skill.is_techical = form.techical.data     
        
        db.session.commit()
        flash('Edited', 'success')
        return redirect(url_for('.manage_bio'))
    form.content.data = skill.content
    form.techical.data = skill.is_techical
    return render_template('manage/edit_bio.html', form=form, title='Skill')

@manage_blueprint.route('/work/<int:work_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_work(work_id):
    form = work_form()
    work = Work_.query.get(work_id)
    if form.validate_on_submit():
        work.title = form.title.data 
        work.company = form.company.data
        work.time = form.time.data   
        work.abstract = form.body.data   
        db.session.commit()
        flash('Edited', 'success')
        return redirect(url_for('.manage_bio'))
    form.title.data  = work.title
    form.company.data = work.company
    form.time.data = work.time
    form.body.data = work.abstract
    return render_template('manage/edit_bio.html', form=form, title='Work Experience')

@manage_blueprint.route('/project/<int:project_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_project(project_id):
    form = project_form()
    project = Project.query.get(project_id)
    if form.validate_on_submit():
        project.title = form.title.data 
        project.role = form.role.data      
        project.abstract = form.body.data   
        
        db.session.commit()
        flash('Edited', 'success')
        return redirect(url_for('.manage_bio'))
    form.title.data = project.title
    form.role.data = project.role
    form.body.data = project.abstract

    return render_template('manage/edit_bio.html', form=form, title='Project')
    

@manage_blueprint.route('/skill/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    work.delete()
    flash('Deleted', 'success')
    return render_template('manage/manage_bio.html')

@manage_blueprint.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.delete()
    flash('Deleted', 'success')
    return render_template('manage/manage_bio.html')

@manage_blueprint.route('/work/<int:work_id>/delete', methods=['POST'])
@login_required
def delete_work(work_id):
    work = Work_.query.get_or_404(work_id)
    work.delete()
    flash('Deleted', 'success')
    return render_template('manage/manage_bio.html')

@manage_blueprint.route('skill/<int:skill_id>/set_techical', methods=['POST'])
@login_required
def set_techical(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.is_techical:
        article.is_techical = False
    else:
        article.is_techical = True
    db.session.commit()
    return redirect_to_last_page()

@manage_blueprint.route('/work/add', methods = ['GET', 'POST'])
@login_required
def add_work():
    form = work_form()
    if form.validate_on_submit():
        title = form.title.data 
        company = form.company.data
        time = form.time.data   
        abstract = form.body.data   
        work = Work_(title=title, company=company, time=time, abstract=abstract) 
        db.session.add(work)
        db.session.commit()
        flash('Added', 'success')
        return redirect(url_for('.manage_bio'))
    return render_template('manage/add_bio.html', form=form, title='Work Experience')
    

@manage_blueprint.route('/skill/add', methods = ['GET', 'POST'])
@login_required
def add_skill():
    form = skill_form()
    if form.validate_on_submit():
        content = form.content.data    
        is_techical = form.techical.data     
        skill = Skill(content=content) 
        db.session.add(skill)
        db.session.commit()
        flash('Added', 'success')
        return redirect(url_for('.manage_bio'))
    return render_template('manage/add_bio.html', form=form, title='Skill')

@manage_blueprint.route('/project/add', methods = ['GET', 'POST'])
@login_required
def add_project():
    form = project_form()
    if form.validate_on_submit():
        title = form.title.data 
        role = form.role.data      
        abstract = form.body.data   
        project = Project(title=title, role=role, abstract=abstract) 
        db.session.add(project)
        db.session.commit()
        flash('Added', 'success')
        return redirect(url_for('.manage_bio'))
    return render_template('manage/add_bio.html', form=form, title='Project')



@manage_blueprint.route('/bio/manage')
@login_required
def manage_bio():
    bio = Bio.query.first()
    works = Work_.query.all()
    projects = Project.query.all()
    skills = Skill.query.all()
    return render_template('manage/manage_bio.html', bio=bio, works=works, projects=projects, skills=skills)

@manage_blueprint.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('This is a default category! Cannot delete!', 'warning')
        return render_template('manage/manage_categories.html')
    category.delete()
    flash('Deleted', 'success')
    return render_template('manage/manage_categories.html')

@manage_blueprint.route('/article/add', methods = ['GET', 'POST'])
@login_required
def add_article():
    form = article_form()
    if form.validate_on_submit():
        title = form.title.data 
        body = form.body.data 
        category = Category.query.get(form.category.data)    
        article = Article(title=title, body=body, category=category, count_read=0)
        db.session.add(article)
        db.session.commit()
        flash('Added', 'success')
        return redirect(url_for('blog.display_article', article_id=article.id))
    return render_template('manage/add_article.html', form=form)

@manage_blueprint.route('/category/new', methods=['GET','POST'])
@login_required
def add_category():
    form = category_form()
    if form.validate_on_submit():
        name = form.name.data 
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Added', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('manage/add_category.html', form=form)

@manage_blueprint.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = category_form()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('This is a default category! Cannot Edit!', 'warning')
        return render_template('manage/manage_category.html')
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("Edited", 'success')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name 
    return render_template('manage/edit_category.html', form=form)

@manage_blueprint.route('article/<int:article_id>/set_comment', methods=['POST'])
@login_required
def set_comment(article_id):
    article = Article.query.get_or_404(article_id)
    if article.comment_open:
        article.comment_open = False
    else:
        article.comment_open = True
    db.session.commit()
    return redirect_to_last_page()

@manage_blueprint.route('/comment/manage')
@login_required
def manage_comment():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MANAGE_COMMENT_PER_PAGE']
    if request.args.get('filter', 'all') == "unreviewed":
        f_comments = Comment.query.filter_by(reviewed=False)
    elif request.args.get('filter', 'all') == "admin":
        f_comments = Comment.query.filter_by(from_admin=True)
    else:
        f_comments = Comment.query
    
    pagination = f_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('manage/manage_comments.html', Article=Article, comments=comments, pagination=pagination)

@manage_blueprint.route('/comment/<int:comment_id>/accept', methods=['POST'])
@login_required
def accept_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    return redirect_to_last_page()


@manage_blueprint.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Deleted', 'success')
    return redirect_to_last_page()


@manage_blueprint.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)

@manage_blueprint.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files.get('upload')
    if not ('.' in file.filename and \
         file.filename.rsplit('.', 1)[1].lower() in \
                 current_app.config['ELIGIBLE_IMAGE']):
        return upload_fail('Can only upload an image(jpg, jpeg, png, gif)')
    file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
    return upload_success(url_for('.get_file', filename=file.filename))

@manage_blueprint.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    file = request.files.get('upload')
    if not ('.' in file.filename and \
             file.filename.rsplit('.', 1)[1].lower() in \
                 current_app.config['ELIGIBLE_PDF']):
        return upload_fail('Can only upload a pdf')
    file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
    return upload_success(url_for('.get_file', filename=file.filename))




    
