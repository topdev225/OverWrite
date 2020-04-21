from flask_mail import Mail, Message
from flask import render_template

from src.models import Order, Account, Role
from conf import conf


mail = Mail()


def send_email(theme: str, recipients: list, text=None, html=None):
    msg = Message(theme, sender=conf["MAIL_USERNAME"], recipients=recipients)
    if text:
        msg.body = text
    elif html:
        msg.html = html
    else:
        raise ValueError
    try:
        mail.send(msg)
    except Exception as e:
        print(e)


def order_email_to_shopper(order: Order, basketImgs: list, basketSizes: list):
    shopper_email = order.checkout_fields.get("Company Email") or order.account.email
    html = render_template(
        "email/order.html", order=order, basketImgs=basketImgs, basketSizes=basketSizes
    )
    send_email("Order", recipients=[shopper_email], html=html)


def order_email_to_ab(order: Order, basketImgs: list, basketSizes: list):
    role = Role.query.filter_by(name="Admin Buyer").first()
    admin_buyer = Account.query.with_parent(order.campaign).filter_by(role=role).first()
    if admin_buyer:
        html = render_template(
            "email/order-notification.html",
            order=order,
            basketImgs=basketImgs,
            basketSizes=basketSizes,
        )
        send_email("New order", recipients=[admin_buyer.email], html=html)
