from app.main import login_manager
from app.accounts.models import Account


@login_manager.user_loader
def load_user(account_id):
    return Account.query.get(account_id)
