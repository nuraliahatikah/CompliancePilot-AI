"""Malaysian Employment Act 1955 and PDPA regulation knowledge base for RAG."""

MALAYSIAN_REGULATIONS: list[dict[str, str]] = [
    {
        "regulation": "Employment Act 1955",
        "section": "Section 12 - Payment of wages",
        "source": "Employment Act 1955 (Act 265)",
        "content": (
            "Every employer shall pay wages to employees not later than the seventh day after "
            "the last day of any wage period. Wages shall be paid in legal tender or by cheque "
            "payable on demand. Deductions from wages are only permitted as authorized under "
            "this Act. Failure to pay wages on time constitutes an offence."
        ),
    },
    {
        "regulation": "Employment Act 1955",
        "section": "Section 60A - Hours of work",
        "source": "Employment Act 1955 (Act 265)",
        "content": (
            "An employee shall not be required to work more than eight hours in one day or "
            "more than forty-five hours in one week. Overtime work shall be paid at a rate "
            "not less than one and a half times the hourly rate of pay. Rest days and public "
            "holidays must be observed as prescribed."
        ),
    },
    {
        "regulation": "Employment Act 1955",
        "section": "Section 60F - Annual leave",
        "source": "Employment Act 1955 (Act 265)",
        "content": (
            "Every employee is entitled to paid annual leave. An employee who has been employed "
            "for less than two years is entitled to not less than eight days; between two and "
            "five years, not less than twelve days; and more than five years, not less than "
            "sixteen days of annual leave per year."
        ),
    },
    {
        "regulation": "Employment Act 1955",
        "section": "Section 37 - Termination and notice",
        "source": "Employment Act 1955 (Act 265)",
        "content": (
            "Either party to a contract of service may terminate the contract by giving notice "
            "or paying wages in lieu of notice. The notice period depends on length of service: "
            "four weeks if employed less than two years, six weeks if between two and five years, "
            "and eight weeks if employed five years or more."
        ),
    },
    {
        "regulation": "Employment Act 1955",
        "section": "Section 60I - Maternity leave",
        "source": "Employment Act 1955 (Act 265)",
        "content": (
            "Every female employee is entitled to maternity leave for a period of not less than "
            "ninety-eight consecutive days. An employer shall not terminate the service of a "
            "female employee during her pregnancy or while on maternity leave except for "
            "willful breach of contract, misconduct, or closure of business."
        ),
    },
    {
        "regulation": "Employment Act 1955",
        "section": "Section 24 - Prohibition of forced labour",
        "source": "Employment Act 1955 (Act 265)",
        "content": (
            "Any term of a contract of service or contract for service which provides for "
            "compulsory labour or which prevents an employee from terminating his contract "
            "of service shall be void. No employer shall require any employee to work beyond "
            "the limits prescribed without proper compensation."
        ),
    },
    {
        "regulation": "Employment Act 1955",
        "section": "Section 60D - Rest day",
        "source": "Employment Act 1955 (Act 265)",
        "content": (
            "Every employee shall be allowed in each week a rest day which shall consist of "
            "one whole day. Where an employee is required to work on a rest day, he shall "
            "be paid at a rate not less than two times his hourly rate of pay."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 6 - General Principle",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "A data user shall not process personal data of a data subject unless the data "
            "subject has given consent to the processing of the personal data. Processing "
            "must be for a lawful purpose directly related to an activity of the data user."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 7 - Notice and Choice Principle",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "A data user shall by written notice inform a data subject that personal data "
            "is being processed, the purpose, and the right to request access and correction. "
            "The notice must be given before or at the time of collecting personal data."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 9 - Security Principle",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "A data user shall take practical steps to protect personal data from any loss, "
            "misuse, modification, unauthorized or accidental access or disclosure, alteration "
            "or destruction by having regard to the nature of the data and the harm that might "
            "result from such an event."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 10 - Retention Principle",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "Personal data processed for any purpose shall not be kept longer than is necessary "
            "for the fulfillment of that purpose. Data users must take reasonable steps to "
            "ensure that personal data is destroyed or permanently deleted when no longer required."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 11 - Data Integrity Principle",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "A data user shall take reasonable steps to ensure that the personal data is "
            "accurate, complete, not misleading and kept up-to-date. Data subjects have the "
            "right to request correction of inaccurate personal data."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 12 - Access Principle",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "A data user shall upon request by a data subject provide access to his personal "
            "data and allow correction where the data is inaccurate, incomplete, misleading "
            "or not up-to-date. Access requests must be responded to within twenty-one days."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 130 - Cross-border transfer",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "A data user shall not transfer personal data to a place outside Malaysia unless "
            "to such a place specified by the Minister or the data user has ensured that the "
            "place has a law substantially similar to the PDPA or the data subject has "
            "consented to the transfer."
        ),
    },
    {
        "regulation": "Personal Data Protection Act 2010",
        "section": "Section 5 - Sensitive Personal Data",
        "source": "PDPA 2010 (Act 709)",
        "content": (
            "Sensitive personal data includes information about physical or mental health, "
            "political opinions, religious beliefs, commission of offences, and other "
            "categories prescribed. Explicit consent is required before processing sensitive "
            "personal data unless an exemption applies."
        ),
    },
]
