import json
import logging
import urllib
import urllib2

zapier_incoming = ''


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    reg = event["registration"]
    name = reg["name"]
    email = event["email"]
    currency = reg["currency"]
    total_cost = reg["total"]
    ticket_type = reg["release_title"]
    ticket_discount_code = event["discount_code_used"]
    ticket_quantity = sum(r["quantity"] for r in reg["receipt"]["receipt_lines"])
    ticket_cost = event["price"]
    payment_email = reg["email"]

    body = dict(
      title=event["event"]["title"],
      url=event["event"]["url"],
      name=name,
      email=email,
      payment_email=payment_email,
      currency=currency,
      total_cost=total_cost,
      ticket_discount_code=ticket_discount_code,
      ticket_quantity=ticket_quantity,
      ticket_cost=ticket_cost,
      ticket_type=ticket_type)

    data = urllib.urlencode(body)

    returned = urllib2.urlopen(zapier_incoming, data)
    try:
      return returned.read()
    finally:
      returned.close()
