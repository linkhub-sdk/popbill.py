__version__ = '1.4.0'
Version = __version__  # for backward compatibility
__all__ = [ "PopbillException","JoinForm","ContactInfo","CorpInfo",
			"TaxinvoiceService","Taxinvoice","TaxinvoiceDetail","Contact",
			"FaxService","FaxReceiver",
			"StatementService", "Statement","StatementDetail",
			"CashbillService", "Cashbill",
			"MessageService", "MessageReceiver",
            "HTTaxinvoiceService", "HTCashbillService",
            "ClosedownService"]

from .base import PopbillException , JoinForm, ContactInfo, CorpInfo
from .taxinvoiceService import *
from .statementService import *
from .faxService import *
from .cashbillService import *
from .messageService import *
from .htTaxinvoiceService import *
from .htCashbillService import *
from .closedownService import *
