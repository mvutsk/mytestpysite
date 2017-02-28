from flask import Blueprint, render_template, session, g, flash, request, redirect, url_for, current_app
from common.acc_models import User, Friend, friend_list
from common.utils import get_signer
from accounts.acc_forms import LoginForm, SignupForm, SignupConfirmForm, RecoverPasswordForm, \
     RecoverPasswordConfirmForm, FriendForm

accounts_prj = Blueprint('accounts_prj', __name__)


@accounts_prj.before_app_request
def load_user():
    g.user = None
    if 'user_id' in session:
        try:
            g.user = User.objects.get(pk=session['user_id'])
        except:
            pass


@accounts_prj.route('/login/', methods=['GET', 'POST'])
def login():
    next = request.values.get('next', '/')
    form = LoginForm()
    form.next.data = next
    if form.validate_on_submit():
        # session['user_id'] = unicode(form.user.pk)
        session['user_id'] = str(form.user.pk)
        fmsg = "Login successfully. Last time you was here at "
        fmsg += str(form.user.last_login)
        flash(fmsg, 'success')
        form.user.refresh_last_login()
        session['logged_in'] = True
        return redirect(next)
    return render_template('accounts/login.html', form=form)


@accounts_prj.route('/logout/')
def logout():
    next = request.args.get('next', '/')
    flash('Logout successfully', 'success')
    session.pop('user_id', None)
    return redirect(next)


@accounts_prj.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if current_app.config['MAIL_FAKE_LINK'] != 'True':
            form.save()
            flash(
                'Check your email to confirm registration.',
                'success'
            )
        else:
            sign_data = form.save()
            flash_msg = "It is a debug mode, so we pretended that sent this to your email to confirm activation:\n\n"
            flash_msg += current_app.config['PROJECT_SITE_URL']
            flash_msg += url_for('accounts_prj.signup_confirm', token=sign_data) + "\n"
            flash(flash_msg, 'success')
        return redirect(url_for('posts_prj.index'))
    return render_template('accounts/signup.html', form=form)


@accounts_prj.route('/signup/<token>/', methods=['GET', 'POST'])
def signup_confirm(token):
    s = get_signer()
    try:
        signed_data = s.loads(
            token, max_age=current_app.config['PROJECT_SIGNUP_TOKEN_MAX_AGE']
        )
        email = signed_data['email']
        signup = signed_data['signup']
    except:
        flash('Invalid activation Link.', 'error')
        return redirect(url_for('accounts_prj.signup'))

    if User.objects.filter(email=email):
        flash('E-mail in use.', 'error')
        return redirect(url_for('accounts_prj.signup'))

    next = request.values.get('next', '/')

    form = SignupConfirmForm()
    form.next.data = next
    if form.validate_on_submit():
        user = form.save(email=email)
        session['user_id'] = str(user.pk)
        flash('Account registered successfully.', 'success')
        return redirect(next)
    return render_template('accounts/signup_confirm.html', form=form, token=token)


@accounts_prj.route('/recover-password/', methods=['GET', 'POST'])
def recover_password():
    form = RecoverPasswordForm()
    if form.validate_on_submit():
        if current_app.config['MAIL_FAKE_LINK'] != 'True':
            form.save()
            flash(
                'Check it out at your email instructions for setting a new password.',
                'success'
            )
            return redirect(url_for('posts_prj.index'))
        else:
            sign_data = form.save()
            flash_msg = "It is a debug mode, so we pretended that sent this to your email to confirm activation:\n\n"
            flash_msg += current_app.config['PROJECT_SITE_URL']
            flash_msg += url_for('accounts_prj.recover_password_confirm', token=sign_data) + "\n"
            flash(flash_msg, 'success')
            return redirect(url_for('posts_prj.index'))
    return render_template('accounts/recover_password.html', form=form)


@accounts_prj.route('/recover-password/<token>/', methods=['GET', 'POST'])
def recover_password_confirm(token):
    s = get_signer()
    try:
        signed_data = s.loads(
            token, max_age=current_app.config['PROJECT_RECOVER_PASSWORD_TOKEN_MAX_AGE']
        )
        email = signed_data['email']
        recover_password = signed_data['recover-password']
    except:
        flash('Invalid Link.', 'error')
        return redirect(url_for('posts_prj.index'))

    try:
        user = User.objects.get(email=email)
    except:
        flash('E-mail not found.', 'error')
        return redirect(url_for('posts_prj.index'))

    form = RecoverPasswordConfirmForm()
    form.user = user
    if form.validate_on_submit():
        user = form.save()
        flash('Password set successfully.', 'success')
        return redirect(url_for('accounts_prj.login'))
    return render_template(
        'accounts/recover_password_confirm.html',
        form=form, token=token, user=user
    )


def listOfFriends(user):
    isfriend = []
    lfriend = []
    if user.friends:
        for fu_id in user.friends:
            fr = friend_list()
            try:
                fuser = User.objects.get(id=fu_id.friend_user_id)
            except:
                fuser = None
            if fuser:
                fr.name = fuser.name
                fr.username = fuser.username
                fr.status = fu_id.status
                fr.added_at = fu_id.added_at
            else:
                fr.name = fu_id.friend_user_id
                fr.username = "Removed user"
                fr.status = "Removed user"
                fr.added_at = fu_id.added_at
            isfriend.append(str(fu_id.friend_user_id))
            lfriend.append(fr)
    return (lfriend, isfriend)


@accounts_prj.route('/profile/<username>/', methods=['GET', 'POST'])
def user_profile(username):
    """isfriend = notfriend
                = requested
                = friend
                = yourself"""
    user = User.objects.get_or_404(username=username)
    if str(user.id) == session.get('user_id', None):
        return redirect(url_for('accounts_prj.myprofile'))
    (lfriend, isfriendList) = listOfFriends(user)
    if str(session.get('user_id', None)) in isfriendList:
        isfriend = 'friend'
    else:
        isfriend = 'notfriend'

    return render_template('accounts/view_profile.html',
                           user=user, lfriends=lfriend, isfriend=isfriend)

@accounts_prj.route('/myprofile/', methods=['GET', 'POST'])
def myprofile():
    """
    :return:
    """
    user = User.objects.get_or_404(id=session.get('user_id', None))

    (lfriend, isfriend) = listOfFriends(user)

    return render_template('accounts/view_myprofile.html', user=user, lfriends=lfriend)


@accounts_prj.route('/ask4friend/<fusername>', methods=['GET', 'POST'])
def ask4friend(fusername):
    """
    requestor - who requesting a friendship
    initiator - from who user requested a friendship

    addtofriend - initial request for friendship, pair (requestor, initiator)
    confirmfriend - confirmation of friendship (requestor)
    rejectfriendask - rejecting friendship request (requestor)
    cancelfriendask - canceling reqiest for friendship (initiator)
    removefriend - removing friend

    :param fusername: is the username which user add/removes to friends
    :return:
    """
    if session.get('user_id', None):

        exectype = request.args.get('action', None)
        if exectype:
            try:
                initiator_user = User.objects.get(pk=session.get('user_id', None))
            except:
                flash("Could not find your session, try to relogin.", 'error')
                return redirect(url_for('accounts_prj.user_profile', username=fusername))

            try:
                fuser = User.objects.get(username=fusername)
            except:
                flash("Could not find this user " + fusername + ". Is user alive?", 'error')
                return redirect(url_for('accounts_prj.user_profile', username=fusername))

        if exectype == 'addtofriend':

            ffuser = Friend(friend_user_id=initiator_user.id, status='initiator')
            finitiator_user = Friend(friend_user_id=fuser.id, status='requested')

            fuser.friends.append(ffuser)
            initiator_user.friends.append(finitiator_user)

            fuser.save()
            initiator_user.save()

            flash("Request for friendship sent to user", 'success')
            return redirect(url_for('accounts_prj.user_profile', username=fusername))

        elif exectype == 'confirmfriend':

            for ffrnds in fuser.friends:
                if str(ffrnds.friend_user_id) == str(initiator_user.id):
                    ffrnds.status = 'friend'
                    break

            for ffrnds in initiator_user.friends:
                if str(ffrnds.friend_user_id) == str(fuser.id):
                    ffrnds.status = 'friend'
                    break

            fuser.save()
            initiator_user.save()

            flash_msg = "You are friends now with " + fusername
            flash(flash_msg, 'success')
            return redirect(url_for('accounts_prj.myprofile'))

        elif exectype == 'rejectfriendask':

            if str(fuser.id) == str(initiator_user.id):
                flash('You could not reject it.', 'error')
                return redirect(url_for('accounts_prj.myprofile'))

            for ffrnds in fuser.friends:
                if str(ffrnds.friend_user_id) == str(initiator_user.id):
                    fuser.friends.remove(ffrnds)
                    break

            for ffrnds in initiator_user.friends:
                if str(ffrnds.friend_user_id) == str(fuser.id):
                    initiator_user.friends.remove(ffrnds)
                    break

            fuser.save()
            initiator_user.save()

            flash_msg = "You have rejected request for frinedship from " + fusername
            flash(flash_msg, 'success')
            return redirect(url_for('accounts_prj.myprofile'))

        elif exectype == 'cancelfriendask':

            if str(fuser.id) == str(initiator_user.id):
                flash('You could not cancel it.', 'error')
                return redirect(url_for('accounts_prj.myprofile'))

            for ffrnds in fuser.friends:
                if str(ffrnds.friend_user_id) == str(initiator_user.id):
                    fuser.friends.remove(ffrnds)
                    break

            for ffrnds in initiator_user.friends:
                if str(ffrnds.friend_user_id) == str(fuser.id):
                    initiator_user.friends.remove(ffrnds)
                    break

            fuser.save()
            initiator_user.save()

            flash_msg = "Request for friendship to {} canceled ".format(fusername)
            flash(flash_msg, 'success')
            return redirect(url_for('accounts_prj.myprofile'))

        elif exectype == 'removefriend':

            for ffrnds in fuser.friends:
                if str(ffrnds.friend_user_id) == str(initiator_user.id):
                    fuser.friends.remove(ffrnds)
                    break

            for ffrnds in initiator_user.friends:
                if str(ffrnds.friend_user_id) == str(fuser.id):
                    initiator_user.friends.remove(ffrnds)
                    break

            fuser.save()
            initiator_user.save()

            flash_msg = "You have removed {} from your friends ".format(fusername)
            flash(flash_msg, 'success')
            return redirect(url_for('accounts_prj.myprofile'))

        else:
            flash("What do you want?", 'error')
            return redirect(url_for('accounts_prj.user_profile', username=fusername))

    else:
        flash("Please login for asking a friendship.", 'error')
        return redirect(url_for('accounts_prj.user_profile', username=fusername))


@accounts_prj.route('/all-users/', methods=['GET', 'POST'])
def all_users():
    """
    Shows all registered users on the site.
    :return: list of registered users
    """
    if not session.get('user_id', None):
        flash("Please login for viewing this page.", 'error')
        users = None
    else:
        try:
            users = User.objects.all()
        except:
            users = None

    return render_template('accounts/view_all_users.html', users=users)


@accounts_prj.route('/reset-password/', methods=['GET', 'POST'])
def reset_password():
    """
    Allows to reset password for user.
    :return:
    """
    if session.get('user_id', None):
        try:
            user = User.objects.get(pk=session.get('user_id', None))
        except:
            flash("Could not find your account by username. Try to recover.", 'error')
            return redirect(url_for('accounts_prj.recover_password'))

        form = RecoverPasswordConfirmForm()
        form.user = user
        if form.validate_on_submit():
            user = form.save()
            user.save()
            flash('Password set successfully.', 'success')
            return redirect(url_for('accounts_prj.myprofile'))
        return render_template('accounts/recover_password_confirm.html', form=form, user=user)
    else:
        flash('You need to login to reset something.', 'error')
        return redirect(url_for('accounts_prj.login'))

@accounts_prj.errorhandler(404)
def page_not_found(error):
    return 'The Force is not with you here.', 404
