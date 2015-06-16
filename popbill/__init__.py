__version__ = '1.1.2'
Version = __version__  # for backward compatibility
__all__ = [ "PopbillException","JoinForm",
			"TaxinvoiceService","Taxinvoice","TaxinvoiceDetail","Contact",
			"FaxService","FaxReceiver",
			"StatementService", "Statement","StatementDetail",
			"CashbillService", "Cashbill",
			"MessageService", "MessageReceiver"]

from .base import PopbillException , JoinForm
from .taxinvoiceService import *
from .statementService import *
from .faxService import *
from .cashbillService import *
from .messageService import * 
