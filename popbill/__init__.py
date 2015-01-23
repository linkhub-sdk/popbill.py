__version__ = '1.0.0'
Version = __version__  # for backward compatibility
__all__ = [ "PopbillException","JoinForm",
			"TaxinvoiceService","Taxinvoice","TaxinvoiceDetail","Contact",
			"FaxService","FaxReceiver"]

from .base import PopbillException , JoinForm
from .taxinvoiceService import *
from .faxService import *