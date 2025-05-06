from flask import redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, FriendRequest
from . import main  # Import the Blueprint

@main.route('/friend-request/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_request(request_id):
    request = FriendRequest.query.get_or_404(request_id)
    current_user.accept_friend_request(request)
    flash("Friend request accepted.")
    return redirect(url_for('main.friend_requests'))

@main.route('/friend-request/send/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    receiver = User.query.get_or_404(user_id)
    try:
        current_user.send_friend_request(receiver)
        flash("Friend request sent.")
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.find_friends'))

@main.route('/friend-request/<int:request_id>/deny', methods=['POST'])
@login_required
def deny_request(request_id):
    request = FriendRequest.query.get_or_404(request_id)
    try:
        current_user.deny_friend_request(request)
        flash('Friend request denied.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.friend_requests'))

@main.route('/friend-request/<int:request_id>/cancel', methods=['POST'])
@login_required
def cancel_request(request_id):
    request = FriendRequest.query.get_or_404(request_id)
    try:
        current_user.cancel_friend_request(request)
        flash('Friend request canceled.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.friend_requests'))

@main.route('/friend/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    friend = User.query.get_or_404(user_id)
    try:
        current_user.remove_friend(friend)
        flash('Friend removed.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.manage_friends'))

