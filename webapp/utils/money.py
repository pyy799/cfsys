# coding: utf-8

from webapp import log
from webapp.const import InvoiceStatus
from webapp.models import Invoice, Contract, BackMoney


def get_invoice_total(con):
    """
    获得一个合同的全部已开票的发票价格
    """
    invoice = Invoice.objects.filter(contract__id=con, status=InvoiceStatus.INVOICED)
    money = [i.money for i in invoice]
    return float("%.2f" % sum(money))


def get_no_invoice_total(con):
    """
    获得合同未开票的金额
    """
    invoice_total = get_invoice_total(con)
    try:
        contract = Contract.objects.get(id=con)
    except Exception as e:
        log.log_error(e)
        return 0

    contract_total = contract.total_money
    no_invoice_total = contract_total - invoice_total
    return no_invoice_total


def get_back_total(con):
    """
    全部的回款金额
    """
    back = BackMoney.objects.filter(contract__id=con)
    money = [i.money for i in back]
    return float("%.2f" % sum(money))


def get_invoice_noback_total(con):
    """
    发票未回款
    """
    invoice_money = get_invoice_total(con)
    back_money = get_back_total(con)
    money = invoice_money - back_money
    return money


def get_contract_noback_total(con):
    """
    合同未回款
    """
    try:
        contract = Contract.objects.get(id=con)
    except Exception as e:
        log.log_error(e)
        return 0

    contract_money = contract.total_money
    back_money = get_back_total(con)
    money = contract_money - back_money
    return money
