from datetime import datetime

def nda_template(company_1, company_2, scope, jurisdiction, effective_date=None, extra_clauses=""):
    today = datetime.today().strftime("%B %d, %Y")
    effective = effective_date or today

    return f"""
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (this "Agreement") is made effective as of {effective}, by and between {company_1} (the "Owner") and {company_2} (the "Recipient").

The parties agree to the following:

1. CONFIDENTIAL INFORMATION  
The term "Confidential Information" includes proprietary, technical, business, and other information disclosed by the Owner that is not generally known to the public.

1.1. "Confidential Information" does not include:  
- Publicly known information;  
- Information received from a third party without confidentiality obligations;  
- Information independently developed by the Recipient;  
- Information required to be disclosed by law.  

2. PROTECTION OF CONFIDENTIAL INFORMATION  
The Recipient shall maintain the confidentiality of the information received and take all reasonable precautions to protect it.

2.1. No Disclosure: The Recipient shall not disclose Confidential Information to third parties without prior written consent of the Owner.  
2.2. No Copying/Modifying: The Recipient shall not copy, reproduce, or alter Confidential Information.  
2.3. Unauthorized Use: The Recipient shall notify the Owner promptly if it becomes aware of any unauthorized use or disclosure.  
2.4. Application to Employees: The Recipient shall ensure employees accessing Confidential Information are bound by this Agreement.  

3. RETURN OF CONFIDENTIAL INFORMATION  
Upon request, the Recipient shall return or destroy all Confidential Information and certify compliance.

4. TERM  
This Agreement remains effective for two (2) years from the Effective Date, and confidentiality obligations survive for two (2) years after termination.

5. JURISDICTION  
This Agreement shall be governed by the laws of {jurisdiction}, and any disputes shall be resolved in its courts.

{extra_clauses.strip() if extra_clauses else ""}

6. ENTIRE AGREEMENT  
This Agreement contains the full understanding between the Parties and supersedes all prior agreements.

7. SIGNATORIES  
IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

OWNER:  
{company_1}  
By: _______________________        Date: _______________

RECIPIENT:  
{company_2}  
By: _______________________        Date: _______________
"""
